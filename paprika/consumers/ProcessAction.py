import json
from datetime import datetime, timedelta
from paprika.consumers.Consumable import Consumable
from paprika.messaging.Message import Message
from paprika.processing.ProcessService import ProcessService
from paprika.repositories.ProcessActionPropertyRepository import ProcessActionPropertyRepository
from paprika.repositories.ProcessActionRepository import ProcessActionRepository
from paprika.repositories.ProcessDefinitionActionPropertyRepository import ProcessDefinitionActionPropertyRepository
from paprika.repositories.ProcessDefinitionActionRepository import ProcessDefinitionActionRepository
from paprika.repositories.ProcessPropertyRepository import ProcessPropertyRepository
from paprika.repositories.ProcessRepository import ProcessRepository
from paprika.system.ClassLoader import ClassLoader
from paprika.system.Traceback import Traceback
from paprika.system.logger.Logger import Logger


class ProcessAction(Consumable):
    def __init__(self):
        Consumable.__init__(self)

    def action(self, connector, message):
        try:
            process_action = json.loads(message['payload'])
            process_action_repository = ProcessActionRepository(connector)

            # set the state of the process action
            process_action['state'] = 'PROCESSING'
            process_action['message'] = ''
            process_action['backtrace'] = ''
            process_action_repository.state(process_action)

            process_action_property_repository = ProcessActionPropertyRepository(connector)
            action = ClassLoader.find(process_action_property_repository.get_property(process_action, 'action'))
            payload = action.execute(connector, process_action)
            if payload:
                process_repository = ProcessRepository(connector)
                process_action_property_repository = ProcessActionPropertyRepository(connector)
                process = process_repository.find_by_id(payload['pcs_id'])
                sleep = float(process_action_property_repository.get_property(process_action, 'sleep'))
                now = datetime.now()
                delay = now + timedelta(seconds=int(sleep))
                delay = delay.strftime('%Y-%m-%d %H:%M:%S')
                Message.enqueue_wait(connector, process['queue'], delay, payload, 'message', 'paprika.consumers.ProcessAction.ProcessAction')
            else:
                process_repository = ProcessRepository(connector)
                process = process_repository.find_by_id(process_action['pcs_id'])
                process_definition_action_repository = ProcessDefinitionActionRepository(connector)
                process_definition_action = process_definition_action_repository.find_next_by_process_action(process_action, process)
                if process_definition_action:
                    next_process_action = dict()
                    next_process_action['job_name'] = process_action['job_name']
                    next_process_action['pcs_id'] = process_action['pcs_id']
                    next_process_action['dan_id'] = process_definition_action['id']
                    next_process_action['name'] = process_definition_action['name']
                    next_process_action['state'] = 'READY'
                    next_process_action = process_action_repository.insert(next_process_action)

                    process_definition_action_property_repository = ProcessDefinitionActionPropertyRepository(connector)
                    process_definition_action_properties = process_definition_action_property_repository.list_by_process_definition_action(process_definition_action)
                    for process_definition_action_property in process_definition_action_properties:
                        process_action_property_repository.set_property(next_process_action, process_definition_action_property['name'], process_definition_action_property['value'])

                    payload = next_process_action
                    Message.enqueue(connector, process['queue'], payload, 'message', 'paprika.consumers.ProcessAction.ProcessAction')
                else:
                    payload = process_repository.find_by_id(process_action['pcs_id'])
                    Message.enqueue(connector, process['queue'], payload, 'message', 'paprika.consumers.ProcessFinish.ProcessFinish')

                process_action['state'] = 'PROCESSED'
                process_action['message'] = ''
                process_action['backtrace'] = ''
                process_action_repository.state(process_action)
        except:
            # set the process_action to failed
            process_action = json.loads(message['payload'])
            process_action_repository = ProcessActionRepository(connector)
            result = Traceback.build()
            result['id'] = process_action['id']
            result['state'] = 'FAILED'
            process_action_repository.state(result)

            # set the process to failed
            process_repository = ProcessRepository(connector)
            process = process_repository.find_by_id(process_action['pcs_id'])
            result['id'] = process['id']
            result['state'] = 'FAILED'
            process_repository.state(result)

            # log a fatal of the process
            logger = Logger(connector, self)
            logger.fatal(process['job_name'], result['message'], result['backtrace'])

            # start the exception process if present
            if process['e_pdn_id']:
                e_process = ProcessService.create_process(connector, process['e_pdn_id'], process['job_name'])

                process_property_repository = ProcessPropertyRepository(connector)
                process_property_repository.copy(process, e_process)
                process_property_repository.set_property(e_process, 'message', result['message'])
                process_property_repository.set_property(e_process, 'backtrace', result['backtrace'])

                ProcessService.execute_process(connector, e_process)

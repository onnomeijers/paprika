import json
from paprika_connector.connectors.DatasourceBuilder import DatasourceBuilder
from paprika.consumers.Consumable import Consumable
from paprika.messaging.Message import Message
from paprika.repositories.ProcessActionPropertyRepository import ProcessActionPropertyRepository
from paprika.repositories.ProcessActionRepository import ProcessActionRepository
from paprika.repositories.ProcessDefinitionActionPropertyRepository import ProcessDefinitionActionPropertyRepository
from paprika.repositories.ProcessDefinitionActionRepository import ProcessDefinitionActionRepository
from paprika.repositories.ProcessDefinitionRepository import ProcessDefinitionRepository
from paprika.repositories.ProcessRepository import ProcessRepository
from paprika.system.Traceback import Traceback
from paprika.system.logger.Logger import Logger


class ProcessStart(Consumable):
    def __init__(self):
        Consumable.__init__(self)

    def action(self, connector, message):
        try:
            process = json.loads(message['payload'])
            process_repository = ProcessRepository(connector)

            process['state'] = 'PROCESSING'
            process['message'] = ''
            process['backtrace'] = ''
            process_repository.state(process)

            process_definition_repository = ProcessDefinitionRepository(connector)
            process_definition_action_repository = ProcessDefinitionActionRepository(connector)
            process_definition = process_definition_repository.find_by_id(process['pdn_id'])
            process_definition_action = process_definition_action_repository.find_first_by_process_definition(process_definition)

            process_action_repository = ProcessActionRepository(connector)
            process_action = dict()
            process_action['job_name'] = process['job_name']
            process_action['pcs_id'] = process['id']
            process_action['dan_id'] = process_definition_action['id']
            process_action['name'] = process_definition_action['name']
            process_action['state'] = 'READY'
            process_action = process_action_repository.insert(process_action)

            process_action_property_repository = ProcessActionPropertyRepository(connector)
            process_definition_action_property_repository = ProcessDefinitionActionPropertyRepository(connector)
            process_definition_action_properties = process_definition_action_property_repository.list_by_process_definition_action(process_definition_action)
            for process_definition_action_property in process_definition_action_properties:
                process_action_property_repository.set_property(process_action, process_definition_action_property['name'], process_definition_action_property['value'])

            payload = process_action
            Message.enqueue(connector, process['queue'], payload, 'message', 'paprika.consumers.ProcessAction.ProcessAction')
        except:
            process = json.loads(message['payload'])
            paprika_ds = DatasourceBuilder.build('paprika-ds.json')
            process_repository = ProcessRepository(paprika_ds)
            result = Traceback.build()
            result['id'] = process['id']
            result['state'] = 'FAILED'
            process_repository.state(result)

            logger = Logger(connector, self)
            logger.fatal(process['job_name'], result['message'], result['backtrace'])

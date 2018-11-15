from paprika.repositories.EventRepository import EventRepository
from paprika.repositories.ProcessActionPropertyRepository import ProcessActionPropertyRepository
from paprika.repositories.ProcessPropertyRepository import ProcessPropertyRepository
from paprika.repositories.ProcessRepository import ProcessRepository
from paprika.system.logger.Logger import Logger

from paprika.actions.Actionable import Actionable


class State(Actionable):
    def __init__(self):
        Actionable.__init__(self)

    def execute(self, connector, process_action):

        job_name = process_action['job_name']
        logger = Logger(connector, self)

        event_repository = EventRepository(connector)
        process_repository = ProcessRepository(connector)
        process_property_repository = ProcessPropertyRepository(connector)
        process_action_property_repository = ProcessActionPropertyRepository(connector)

        # retrieve the chunk properties
        process = process_repository.find_by_id(process_action['pcs_id'])
        event_id = process_property_repository.get_property(process, 'event_id')
        message = process_property_repository.get_property(process, 'message')
        backtrace = process_property_repository.get_property(process, 'backtrace')

        event = event_repository.find_by_id(event_id)

        state = process_action_property_repository.get_property(process_action, 'state')
        event['state'] = state
        event['message'] = message
        event['backtrace'] = backtrace
        event_repository.state(event)

        logger.info(job_name, 'job_name: ' + job_name + " state: " + event['state'])

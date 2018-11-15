from paprika.repositories.ProcessPropertyRepository import ProcessPropertyRepository 
from paprika.repositories.ProcessActionPropertyRepository import ProcessActionPropertyRepository
from paprika.system.logger.Logger import Logger

from paprika.actions.Actionable import Actionable


class PurgeProcessesProperties(Actionable):
    def __init__(self):
        Actionable.__init__(self)

    def execute(self, connector, process_action):

        job_name = process_action['job_name']
        logger = Logger(connector, self)

        process_action_property_repository = ProcessActionPropertyRepository(connector)

        # retrieve the properties
        days = process_action_property_repository.get_property(process_action, 'days')

        process_property_repository = ProcessPropertyRepository(connector)
        count = process_property_repository.clean(days)

        logger.info(job_name, str(count) + ' processes_properties record(s) purged.')





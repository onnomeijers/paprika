from paprika.repositories.ProcessActionPropertyRepository import ProcessActionPropertyRepository
from paprika.system.logger.Logger import Logger

from paprika.actions.Actionable import Actionable


class PurgeProcessesActionsProperties(Actionable):
    def __init__(self):
        Actionable.__init__(self)

    def execute(self, connector, process_action):

        job_name = process_action['job_name']
        logger = Logger(connector, self)

        process_action_property_repository = ProcessActionPropertyRepository(connector)

        # retrieve the properties
        days = process_action_property_repository.get_property(process_action, 'days')

        count = process_action_property_repository.clean(days)

        logger.info(job_name, str(count) + ' processes_actions_properties  record(s) purged.')





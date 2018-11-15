from paprika.repositories.LogRepository import LogRepository
from paprika.repositories.ProcessActionPropertyRepository import ProcessActionPropertyRepository
from paprika.system.logger.Logger import Logger

from paprika.actions.Actionable import Actionable


class PurgeLog(Actionable):
    def __init__(self):
        Actionable.__init__(self)

    def execute(self, connector, process_action):

        job_name = process_action['job_name']
        logger = Logger(connector, self)

        process_action_property_repository = ProcessActionPropertyRepository(connector)

        # retrieve the properties
        days = process_action_property_repository.get_property(process_action, 'days')

        log_repository = LogRepository(connector)
        count = log_repository.clean(days)

        logger.info(job_name, str(count) + ' log record(s) purged.')





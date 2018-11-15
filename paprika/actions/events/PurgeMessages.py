from paprika.repositories.MessageRepository import MessageRepository
from paprika.repositories.ProcessActionPropertyRepository import ProcessActionPropertyRepository
from paprika.system.logger.Logger import Logger

from paprika.actions.Actionable import Actionable


class PurgeMessages(Actionable):
    def __init__(self):
        Actionable.__init__(self)

    def execute(self, connector, process_action):

        job_name = process_action['job_name']
        logger = Logger(connector, self)

        process_action_property_repository = ProcessActionPropertyRepository(connector)

        # retrieve the properties
        days = process_action_property_repository.get_property(process_action, 'days')

        message_repository = MessageRepository(connector)
        count = message_repository.clean(days)

        logger.info(job_name, str(count) + ' messages record(s) purged.')





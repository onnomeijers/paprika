from paprika.repositories.ChunkRepository import ChunkRepository
from paprika.repositories.ProcessActionPropertyRepository import ProcessActionPropertyRepository
from paprika.system.logger.Logger import Logger

from paprika.actions.Actionable import Actionable


class PurgeChunks(Actionable):
    def __init__(self):
        Actionable.__init__(self)

    def execute(self, connector, process_action):

        job_name = process_action['job_name']
        logger = Logger(connector, self)

        process_action_property_repository = ProcessActionPropertyRepository(connector)

        # retrieve the properties
        days = process_action_property_repository.get_property(process_action, 'days')

        chunk_repository = ChunkRepository(connector)
        count = chunk_repository.clean(days)

        logger.info(job_name, str(count) + ' chunks record(s) purged.')





from paprika.repositories.ChunkRepository import ChunkRepository
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

        chunk_repository = ChunkRepository(connector)
        process_repository = ProcessRepository(connector)
        process_property_repository = ProcessPropertyRepository(connector)
        process_action_property_repository = ProcessActionPropertyRepository(connector)

        # retrieve the chunk properties
        process = process_repository.find_by_id(process_action['pcs_id'])
        chunk_id = process_property_repository.get_property(process, 'chunk_id')
        message = process_property_repository.get_property(process, 'message')
        backtrace = process_property_repository.get_property(process, 'backtrace')

        chunk = chunk_repository.find_by_id(chunk_id)

        state = process_action_property_repository.get_property(process_action, 'state')
        chunk['state'] = state
        chunk['message'] = message
        chunk['backtrace'] = backtrace
        chunk_repository.state(chunk)

        logger.info(job_name, 'job_name: ' + job_name + " state: " + chunk['state'])
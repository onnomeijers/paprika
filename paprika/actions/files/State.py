from paprika.repositories.FileRepository import FileRepository
from paprika.repositories.ProcessActionPropertyRepository import ProcessActionPropertyRepository
from paprika.repositories.ProcessPropertyRepository import ProcessPropertyRepository
from paprika.repositories.ProcessRepository import ProcessRepository
from paprika.system.logger.Logger import Logger
from paprika.actions.Actionable import Actionable


class State(Actionable):
    def __init__(self):
        Actionable.__init__(self)

    def execute(self, connector, process_action):
        logger = Logger(connector, self)
        job_name = process_action['job_name']

        file_repository = FileRepository(connector)
        process_repository = ProcessRepository(connector)
        process_property_repository = ProcessPropertyRepository(connector)
        process_action_property_repository = ProcessActionPropertyRepository(connector)

        # retrieve the process properties
        process = process_repository.find_by_id(process_action['pcs_id'])
        file_id = process_property_repository.get_property(process, 'file_id')
        message = process_property_repository.get_property(process, 'message')
        backtrace = process_property_repository.get_property(process, 'backtrace')

        file = file_repository.find_by_id(file_id)
        filename = file['filename']

        state = process_action_property_repository.get_property(process_action, 'state')
        if not state:
            state = process_property_repository.get_property(process, 'state')
            if not state:
                state = 'ERROR_NO_STATE'

        file['state'] = state
        file['message'] = message
        file['backtrace'] = backtrace
        file_repository.state(file)

        logger.info(job_name, "filename: " + filename + ", state: " + file['state'])

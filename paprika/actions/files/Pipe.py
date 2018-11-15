from paprika.repositories.FileRepository import FileRepository
from paprika.repositories.ProcessPropertyRepository import ProcessPropertyRepository
from paprika.repositories.ProcessRepository import ProcessRepository
from paprika.system.logger.Logger import Logger
from paprika.actions.Actionable import Actionable


class Pipe(Actionable):
    def __init__(self):
        Actionable.__init__(self)

    def execute(self, connector, process_action):

        job_name = process_action['job_name']
        logger = Logger(connector, self)
        file_repository = FileRepository(connector)
        process_repository = ProcessRepository(connector)
        process_property_repository = ProcessPropertyRepository(connector)

        # retrieve the file properties
        process = process_repository.find_by_id(process_action['pcs_id'])
        file_id = process_property_repository.get_property(process, 'file_id')
        file = file_repository.find_by_id(file_id)
        filename = file['filename']

        locked = file_repository.locked(file)

        if locked:
            logger.info(job_name, 'file: ' + filename + " locked ")
            return process_action
        else:
            logger.info(job_name, 'file: ' + filename + " not locked ")

        logger.info(job_name, filename + " state: " + file['state'])





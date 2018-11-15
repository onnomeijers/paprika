from paprika.repositories.FileRepository import FileRepository
from paprika.repositories.ProcessPropertyRepository import ProcessPropertyRepository
from paprika.repositories.ProcessRepository import ProcessRepository
from paprika.system.logger.Logger import Logger
from paprika.vfs.VfsFactory import VfsFactory
from paprika.actions.Actionable import Actionable
import os


class Delete(Actionable):
    def __init__(self):
        Actionable.__init__(self)

    def execute(self, connector, process_action):
        logger = Logger(connector, self)
        job_name = process_action['job_name']

        process_repository = ProcessRepository(connector)
        process_property_repository = ProcessPropertyRepository(connector)

        file_repository = FileRepository(connector)

        process = process_repository.find_by_id(process_action['pcs_id'])
        file_id = process_property_repository.get_property(process, 'file_id')

        file = file_repository.find_by_id(file_id)

        pickup_location = process_property_repository.get_property(process, 'pickup_location')
        pickup_filename = file['filename']
        pickup_path = process_property_repository.get_property(process, 'path')

        logger.info(job_name, 'filename: ' + pickup_filename + ", pickup_location: " + pickup_location)

        # copy the file from pickup folder to the tmp folder.
        pickup_client = VfsFactory.create_client(pickup_location)
        pickup_client.connect()
        pickup_path = pickup_path + os.sep + pickup_filename
        pickup_client.delete(pickup_path)
        pickup_client.close()

        # set the process properties for the next process_action
        process_property_repository.set_property(process, 'pickup_location', '')
        process_property_repository.set_property(process, 'path', '')

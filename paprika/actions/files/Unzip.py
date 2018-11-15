from paprika.repositories.FileRepository import FileRepository
from paprika.repositories.ProcessActionPropertyRepository import ProcessActionPropertyRepository
from paprika.repositories.ProcessPropertyRepository import ProcessPropertyRepository
from paprika.repositories.ProcessRepository import ProcessRepository
from paprika.repositories.PropertyRepository import PropertyRepository
from paprika.system.logger.Logger import Logger
from paprika.vfs.VfsFactory import VfsFactory
from paprika.actions.Actionable import Actionable
import os


class Unzip(Actionable):
    def __init__(self):
        Actionable.__init__(self)

    def execute(self, connector, process_action):
        job_name = process_action['job_name']
        logger = Logger(connector, self)

        properties = PropertyRepository(connector)
        process_repository = ProcessRepository(connector)
        process_property_repository = ProcessPropertyRepository(connector)
        process_action_property_repository = ProcessActionPropertyRepository(connector)

        file_repository = FileRepository(connector)

        process = process_repository.find_by_id(process_action['pcs_id'])
        file_id = process_property_repository.get_property(process, 'file_id')

        file = file_repository.find_by_id(file_id)

        tmp = properties.get_property('scanner.tmp')

        # retrieve the file properties
        pickup_location = process_property_repository.get_property(process, 'pickup_location')
        pickup_filename = file['filename']
        pickup_path = process_property_repository.get_property(process, 'path')
        drop_location = process_action_property_repository.get_property(process_action, 'drop_location')

        # copy the file from pickup folder to the tmp folder.
        logger.info(job_name, pickup_location + os.sep + pickup_filename)
        pickup_client = VfsFactory.create_client(pickup_location)
        pickup_client.connect()
        pickup_path = pickup_path + os.sep + pickup_filename
        tmp_path = tmp + os.sep + pickup_filename
        pickup_client.get(pickup_path, tmp_path)
        pickup_client.close()

        # unzip the file and copy the unzipped files to the unzip folder
        logger.info(job_name, 'unzip ' + pickup_location + os.sep + pickup_filename)
        zip_client = VfsFactory.create_client("zip://" + tmp_path)
        zip_client.connect()
        zip_files = zip_client.list('')
        for zip_file in zip_files:

            logger.info(job_name, 'unzipping ' + zip_file['path'] + zip_file['filename'])
            zip_client.get(zip_file['path'] + zip_file['filename'], tmp + os.sep + zip_file['path'] + zip_file['filename'])

            # copy the file from the tmp folder to the drop folder
            logger.info(job_name, 'copying ' + tmp + os.sep + zip_file['path'] + zip_file['filename'] + ' to ' + drop_location)
            drop_client = VfsFactory.create_client(drop_location)
            drop_client.connect()

            tmp_path = zip_file['path'] + zip_file['filename']
            drop_path = drop_client.get_path() + os.sep + zip_file['filename']
            drop_client.put(tmp_path, drop_path)
            drop_client.close()

        logger.info(job_name, pickup_location + os.sep + pickup_filename + " unzipped")

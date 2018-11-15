from paprika.repositories.FilePropertyRepository import FilePropertyRepository
from paprika.repositories.ProcessPropertyRepository import ProcessPropertyRepository
from paprika.repositories.ProcessActionPropertyRepository import ProcessActionPropertyRepository
from paprika.repositories.FileRepository import FileRepository
from paprika.actions.Actionable import Actionable
from paprika.system.logger.Logger import Logger
from paprika.repositories.ProcessRepository import ProcessRepository


class Property(Actionable):
    def __init__(self):
        Actionable.__init__(self)

    def execute(self, connector, process_action):
        logger = Logger(connector, self)
        job_name = process_action['job_name']

        # create instances of classes
        file_property_repository = FilePropertyRepository(connector)
        file_repository = FileRepository(connector)
        process_repository = ProcessRepository(connector)
        process_property_repository = ProcessPropertyRepository(connector)
        process_action_property_repository = ProcessActionPropertyRepository(connector)

        # retrieve the required properties
        process = process_repository.find_by_id(process_action['pcs_id'])
        file_id = process_property_repository.get_property(process, 'file_id')
        name = process_action_property_repository.get_property(process_action, 'name')
        value = process_action_property_repository.get_property(process_action, 'value')

        # get the file using the file_id we collected
        file = file_repository.find_by_id(file_id)
        filename = file['filename']

        file_property_repository.set_property(file, name, value)

        logger.info(job_name, "filename: " + filename + ", name: " + name + ", value: " + value)
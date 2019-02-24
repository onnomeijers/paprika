from paprika_connector.connectors.DatasourceBuilder import DatasourceBuilder
from paprika.repositories.FileRepository import FileRepository
from paprika.repositories.ProcessActionPropertyRepository import ProcessActionPropertyRepository
from paprika.repositories.ProcessPropertyRepository import ProcessPropertyRepository
from paprika.repositories.ProcessRepository import ProcessRepository
from paprika.system.logger.Logger import Logger
from paprika.actions.Actionable import Actionable


class FileCsvStageAction(Actionable):
    def __init__(self):
        Actionable.__init__(self)

    def execute(self, process_action):

        job_name = process_action['job_name']

        paprika_ds = DatasourceBuilder.build('paprika-ds.json')
        logger = Logger(self)
        file_repository = FileRepository(paprika_ds)
        process_repository = ProcessRepository(paprika_ds)
        process_property_repository = ProcessPropertyRepository(paprika_ds)
        process_action_property_repository = ProcessActionPropertyRepository(paprika_ds)

        # retrieve the file properties
        process = process_repository.find_by_id(process_action['pcs_id'])
        file_id = process_property_repository.get_property(process, 'file_id')
        file = file_repository.find_by_id(file_id)

        datasource = process_action_property_repository.get_property(process_action, 'datasource')
        drop_location = process_action_property_repository.get_property(process_action, 'drop_location')
        filename = drop_location + '/' + file['filename']

        CsvFile.normalize(filename, filename + '.norm')
        source_encoding = CsvFile.guess_encoding(filename + '.norm')
        CsvFile.iconv(filename + '.norm', source_encoding, filename + '.utf8', 'utf8')
        delimiter = CsvFile.guess_delimiter(filename + '.utf8')

        skip_header = False
        if not header:
            header = CsvFile.read_header(filename + '.utf8', delimiter)
            skip_header = True

        ds = DatasourceBuilder.find(datasource)
        connector = ConnectorFactory.create_connector(ds)

        file_repository = FileRepository(ds)
        file = dict()
        file['pcs_id'] = 0
        file['job_name'] = job_name
        file['filename'] = filename
        file['state'] = 'READY'
        file['rule'] = ''
        file['hashcode'] = ''
        file['pickup_location'] = ''
        file['path'] = ''
        file['filesize'] = 0
        file['pattern'] = ''
        file = file_repository.insert(file)

        statics = dict()
        statics['job_name'] = job_name
        statics['fle_id'] = file['id']

        mapping = 'id.eeid;notification.action;job_name.job_name;fle_id.fle_id'

        stager = Stager(ds)
        stager.stage(filename + '.utf8', header, delimiter, 'tripolis_mailings', mapping, skip_header, statics)
        stager.close()

        logger.info(job_name, 'job_name: ' + job_name + 'file: ' + filename + " staged")




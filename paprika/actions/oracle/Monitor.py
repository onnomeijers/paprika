from paprika.actions.Actionable import Actionable
from paprika.repositories.OracleScheduler import OracleScheduler
from paprika.repositories.ProcessActionPropertyRepository import ProcessActionPropertyRepository
from paprika.repositories.ProcessPropertyRepository import ProcessPropertyRepository
from paprika.repositories.ProcessRepository import ProcessRepository
from paprika.system.logger.Logger import Logger
from paprika_connector.connectors.ConnectorFactory import ConnectorFactory
from paprika.repositories.DatasourceRepository import DatasourceRepository


class Monitor(Actionable):
    def __init__(self):
        Actionable.__init__(self)

    def execute(self, connector, process_action):
        logger = Logger(connector, self)
        job_name = process_action['job_name']

        process_repository = ProcessRepository(connector)
        process_property_repository = ProcessPropertyRepository(connector)
        process_action_property_repository = ProcessActionPropertyRepository(connector)

        # retrieve the file properties
        process = process_repository.find_by_id(process_action['pcs_id'])
        identifier = process_property_repository.get_property(process, 'identifier')
        datasource = process_action_property_repository.get_property(process_action, 'datasource')

        datasource_repository = DatasourceRepository(connector)
        oracle_ds = datasource_repository.get_by_name(datasource)
        oracle_c = ConnectorFactory.create_connector(oracle_ds)
        scheduler = OracleScheduler(oracle_c)

        if scheduler.is_running(identifier):
            oracle_c.close()
            return process_action

        # the result should be
        created_at = process['created_at']
        run_result = scheduler.run_result(identifier, job_name, created_at)
        oracle_c.close()

        process_property_repository.set_property(process, 'message', run_result['message'])
        process_property_repository.set_property(process, 'state', run_result['state'])
        process_property_repository.set_property(process, 'backtrace', run_result['backtrace'])

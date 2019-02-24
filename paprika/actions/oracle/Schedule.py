from paprika.actions.Actionable import Actionable
from paprika_connector.connectors.DatasourceBuilder import DatasourceBuilder
from paprika.repositories.FileRepository import FileRepository
from paprika.repositories.OracleScheduler import OracleScheduler
from paprika.repositories.ProcessActionPropertyRepository import ProcessActionPropertyRepository
from paprika.repositories.ProcessPropertyRepository import ProcessPropertyRepository
from paprika.repositories.ProcessRepository import ProcessRepository
from paprika.system.logger.Logger import Logger
from paprika_connector.connectors.ConnectorFactory import ConnectorFactory
from paprika.system.ExpressionParser import ExpressionParser
from paprika.system.Strings import Strings
import json


class Schedule(Actionable):
    def __init__(self):
        Actionable.__init__(self)

    def execute(self, connector, process_action):
        logger = Logger(connector, self)
        job_name = process_action['job_name']

        file_repository = FileRepository(connector)
        process_repository = ProcessRepository(connector)
        process_property_repository = ProcessPropertyRepository(connector)
        process_action_property_repository = ProcessActionPropertyRepository(connector)

        # retrieve the file properties
        process = process_repository.find_by_id(process_action['pcs_id'])

        payload = process_property_repository.get_property(process, 'payload')
        if payload:
            payload = json.loads(payload)

        datasource = process_action_property_repository.get_property(process_action, 'datasource')
        method_name = process_action_property_repository.get_property(process_action, 'method_name')
        params = process_action_property_repository.get_property(process_action, 'params')
        test_result_params = process_action_property_repository.get_property(process_action, 'test_result_params')
        if params:
            params = json.loads(params)
            params = ExpressionParser.parse(params, locals())

        oracle_ds = DatasourceBuilder.find(connector, datasource)
        oracle_c = ConnectorFactory.create_connector(oracle_ds)
        scheduler = OracleScheduler(oracle_c)

        identifier = job_name + '_' + Strings.identifier(10)

        message = dict()
        message['method_name'] = method_name
        message['identifier'] = identifier
        message['params'] = params
        if test_result_params:
            message['test_result_params'] = json.loads(test_result_params)
        scheduler.create_job(message)

        logger.info(job_name, json.dumps(message))

        process_property_repository.set_property(process, 'identifier', identifier)
        oracle_c.close()

from paprika.actions.Actionable import Actionable
from paprika.repositories.ProcessActionPropertyRepository import ProcessActionPropertyRepository
from paprika.repositories.ProcessPropertyRepository import ProcessPropertyRepository
from paprika.repositories.ProcessRepository import ProcessRepository
from paprika.system.logger.Logger import Logger
from paprika_connector.connectors.ConnectorFactory import ConnectorFactory
from paprika.repositories.OracleCall import OracleCall
from paprika.system.ExpressionParser import ExpressionParser
import json
from paprika.repositories.DatasourceRepository import DatasourceRepository


class Call(Actionable):
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

        # retrieve the payload if present
        payload = process_property_repository.get_property(process, 'payload')
        if payload:
            payload = json.loads(payload)

        datasource = process_action_property_repository.get_property(process_action, 'datasource')
        method_name = process_action_property_repository.get_property(process_action, 'method_name')
        params = process_action_property_repository.get_property(process_action, 'params')
        if params:
            params = json.loads(params)
            params = ExpressionParser.parse(params, locals())

        datasource_repository = DatasourceRepository(connector)
        oracle_ds = datasource_repository.get_by_name(datasource)
        oracle_c = ConnectorFactory.create_connector(oracle_ds)
        oracle_call = OracleCall(oracle_c)

        call = dict()
        call['method_name'] = method_name
        call['params'] = params
        oracle_call.execute(call)

        logger.info(job_name, json.dumps(call))
        oracle_c.close()

        process_property_repository.set_property(process, 'call', json.dumps(call))

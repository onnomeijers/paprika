class ConnectorFactory:
    def __init__(self):
        pass

    @staticmethod
    def create_connector(datasource):
        if datasource['type'] == 'mysql':
            from paprika.connectors.MysqlConnector import MysqlConnector
            return MysqlConnector(datasource)
        if datasource['type'] == 'oracle':
            from paprika.connectors.OracleConnector import OracleConnector
            return OracleConnector(datasource)

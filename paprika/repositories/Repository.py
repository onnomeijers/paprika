class Repository(object):
    def __init__(self, connector):
        object.__init__(self)
        self.__connector = connector

    def get_connector(self):
        return self.__connector

    def get_connection(self):
        connector = self.get_connector()
        connection = connector.get_connection()
        if not connector.is_connected():
            connection = connector.connect()
        return connection

    def statement(self, statement, message):
        connector = self.get_connector()
        return connector.statement(statement, message)

    def has_lastrowid(self):
        connector = self.get_connector()
        datasource = connector.get_datasource()

        if datasource['type'] == 'oracle':
            return False
        return True

from paprika.repositories.Repository import Repository
from paprika_connector.connectors.Helper import Helper


class DatasourceRepository(Repository):
    def __init__(self, connector):
        Repository.__init__(self, connector)

    def get_by_name(self, name):
        connection = self.get_connection()
        cursor = connection.cursor()

        param = dict()
        param['name'] = name

        statement = "select * from datasources where name = :name"
        statement, parameters = self.statement(statement, param)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)

        if len(result) == 0:
            return None
        return result[0]


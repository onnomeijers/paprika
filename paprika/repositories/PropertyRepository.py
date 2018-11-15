from paprika.connectors.Helper import Helper
from paprika.repositories.Repository import Repository


class PropertyRepository(Repository):
    def __init__(self, connector):
        Repository.__init__(self, connector)

    def get_property(self, key):
        connection = self.get_connection()
        cursor = connection.cursor()

        param = dict()
        param['name'] = key

        statement = "select value from application_properties where name = :name"
        statement, parameters = self.statement(statement, param)

        cursor.execute(statement, parameters)
        response = Helper.cursor_to_json(cursor)
        if response:
            record = response[0]
            return record['value']
        else:
            raise Exception('No such property ' + param['name'] + ' in database' + str(connection))

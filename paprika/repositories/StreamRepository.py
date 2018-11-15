from paprika.repositories.Repository import Repository
from paprika.connectors.Helper import Helper


class StreamRepository(Repository):
    def __init__(self, connector):
        Repository.__init__(self, connector)

    def list_active(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("select * from streams where active=1")

        return Helper.cursor_to_json(cursor)

    def list(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("select * from streams")

        return Helper.cursor_to_json(cursor)

    def find_by_hashcode(self, hashcode):
        connection = self.get_connection()
        cursor = connection.cursor()

        param = dict()
        param['hashcode'] = hashcode

        statement = "select * from streams where hashcode = :hashcode"
        statement, parameters = self.statement(statement, param)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)
        cursor.close()

        if len(result) == 0:
            return None
        return result[0]

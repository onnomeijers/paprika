from paprika.connectors.Helper import Helper
from paprika.repositories.Repository import Repository


class ProcessDefinitionRepository(Repository):
    def __init__(self, connector):
        Repository.__init__(self, connector)

    def find_by_id(self, id):
        connection = self.get_connection()
        cursor = connection.cursor()

        param = dict()
        param['id'] = id

        statement = "select * from process_definitions where id = :id"
        statement, parameters = self.statement(statement, param)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)

        if len(result) == 0:
            return None
        return result[0]

    def find_by_hashcode(self, hashcode):
        connection = self.get_connection()
        cursor = connection.cursor()

        param = dict()
        param['hashcode'] = hashcode

        statement = "select * from process_definitions where hashcode = :hashcode"
        statement, parameters = self.statement(statement, param)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)

        if len(result) == 0:
            return None
        return result[0]

    def find_by_name(self, name):
        connection = self.get_connection()
        cursor = connection.cursor()

        param = dict()
        param['name'] = name

        statement = "select * from process_definitions where name = :name"
        statement, parameters = self.statement(statement, param)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)

        if len(result) == 0:
            return None
        return result[0]


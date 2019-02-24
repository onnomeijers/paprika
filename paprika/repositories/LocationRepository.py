from paprika.repositories.Repository import Repository
from paprika_connector.connectors.Helper import Helper


class LocationRepository(Repository):
    def __init__(self, connector):
        Repository.__init__(self, connector)

    def insert(self, message):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = dict()
        params['url'] = message['url']
        params['patterns'] = message['patterns']
        params['recursive'] = message['recursive']
        params['depth'] = message['depth']

        statement = "insert into locations(url, patterns, recursive, depth) " \
                    "values (:url, :patterns, :recursive, :depth)"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        message['id'] = cursor.lastrowid
        connection.commit()

        return message

    def list(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("select * from locations")

        return Helper.cursor_to_json(cursor)

    def list_active(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("select * from locations where active=1")

        return Helper.cursor_to_json(cursor)

    def hold(self, message):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = dict()
        params['active'] = message['active']
        params['hashcode'] = message['hashcode']

        statement = "update locations set active = :active where hashcode = :hashcode"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        connection.commit()

    def delete(self, message):
        connection = self.get_connection()
        cursor = connection.cursor()

        param = dict()
        param['hashcode'] = message['hashcode']

        statement = "delete from locations where hashcode = :hashcode"
        statement, parameters = self.statement(statement, message)

        cursor.execute(statement, parameters)
        connection.commit()

    def find_by_hashcode(self, hashcode):
        connection = self.get_connection()
        cursor = connection.cursor()

        param = dict()
        param['hashcode'] = hashcode

        statement = "select * from locations where hashcode = :hashcode"
        statement, parameters = self.statement(statement, param)

        cursor.execute(statement, parameters)

        return Helper.cursor_to_json(cursor)

    def find_by_id(self, id):
        connection = self.get_connection()
        cursor = connection.cursor()

        param = dict()
        param['id'] = id

        statement = "select * from locations where id = :id"
        statement, parameters = self.statement(statement, param)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)

        if len(result) == 0:
            return None
        return result[0]

    def update(self, message):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = dict()
        params['url'] = message['url']
        params['patterns'] = message['patterns']
        params['recursive'] = message['recursive']
        params['depth'] = message['depth']

        statement = "update locations set url = :url, patterns = :patterns, recursive = :recursive, depth = :depth " \
                    "where hashcode = :hashcode"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        connection.commit()

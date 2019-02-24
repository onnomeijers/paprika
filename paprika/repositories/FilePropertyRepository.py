from paprika.repositories.Repository import Repository
from paprika_connector.connectors.Helper import Helper


class FilePropertyRepository(Repository):
    def __init__(self, connector):
        Repository.__init__(self, connector)

    def get_property(self, file, name):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = dict()
        params['fle_id'] = file['id']
        params['name'] = name

        statement = "select * from file_properties where name = :name and fle_id = :fle_id"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)

        if len(result) == 0:
            return None
        return result[0]['value']

    def set_property(self, file, name, value):
        params = dict()
        params['fle_id'] = file['id']
        params['name'] = name
        params['value'] = value

        if self.get_property(file, name):
            self.update(params)
        else:
            self.insert(params)

    def update(self, file_property):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = dict()
        params['fle_id'] = file_property['fle_id']
        params['name'] = file_property['name']

        statement = "update file_properties set value = :value where fle_id = :fle_id and name = :name"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        connection.commit()

    def insert(self, file_property):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = dict()
        params['fle_id'] = file_property['fle_id']
        params['name'] = file_property['name']
        params['value'] = file_property['value']

        statement = "insert into file_properties(fle_id, name, value) values (:fle_id, :name, :value)"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        file_property["id"] = cursor.lastrowid
        connection.commit()

        return file_property

from paprika.repositories.Repository import Repository
from paprika_connector.connectors.Helper import Helper
from datetime import datetime
from datetime import timedelta


class ProcessPropertyRepository(Repository):
    def __init__(self, connector):
        Repository.__init__(self, connector)

    def insert(self, process_property):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = dict()
        params['pcs_id'] = process_property['pcs_id']
        params['name'] = process_property['name']
        params['value'] = process_property['value']

        statement = "insert into processes_properties(pcs_id, name, value) values (:pcs_id, :name, :value)"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        process_property['id'] = cursor.lastrowid
        connection.commit()
        return process_property

    def update(self, process_property):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = dict()
        params['value'] = process_property['value']
        params['pcs_id'] = process_property['pcs_id']
        params['name'] = process_property['name']

        statement = "update processes_properties set value = :value where pcs_id = :pcs_id and name = :name"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        connection.commit()

    def get_property(self, process, name):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = dict()
        params['pcs_id'] = process['id']
        params['name'] = name

        statement = "select value from processes_properties where pcs_id = :pcs_id and name = :name"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)

        if len(result) == 0:
            return None
        return result[0]['value']

    def set_property(self, process, name, value):
        params = dict()
        params['pcs_id'] = process['id']
        params['name'] = name
        params['value'] = value
        if self.get_property(process, name):
            self.update(params)
        else:
            self.insert(params)

    def list_by_process(self, process):
        connection = self.get_connection()
        cursor = connection.cursor()

        param = dict()
        param['pcs_id'] = process['id']

        statement = "select * from processes_properties where pcs_id = :pcs_id"
        statement, parameters = self.statement(statement, param)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)

        if len(result) == 0:
            return None
        return result

    def copy(self, source, target):
        process_properties = self.list_by_process(source)

        for process_property in process_properties:
            self.set_property(target, process_property['name'], process_property['value'])

    def clean(self, days):
        connection = self.get_connection()
        cursor = connection.cursor()

        statement = "delete from processes_properties where created_at <:created_at"

        now = datetime.now()
        window = now - timedelta(days=int(days))
        created_at = window.strftime('%Y-%m-%d %H:%M:%S')

        param = dict()
        param['created_at'] = created_at

        statement, parameters = self.statement(statement, param)

        cursor.execute(statement, parameters)
        count = cursor.rowcount
        cursor.close()
        connection.commit()

        return count

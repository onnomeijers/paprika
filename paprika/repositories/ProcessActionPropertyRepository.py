from paprika.repositories.Repository import Repository
from paprika_connector.connectors.Helper import Helper
from datetime import datetime
from datetime import timedelta


class ProcessActionPropertyRepository(Repository):
    def __init__(self, connector):
        Repository.__init__(self, connector)

    def insert(self, process_action_property):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = dict()
        params['pan_id'] = process_action_property['pan_id']
        params['name'] = process_action_property['name']
        params['value'] = process_action_property['value']

        statement = "insert into processes_actions_properties(pan_id, name, value) values (:pan_id, :name, :value)"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        process_action_property['id'] = cursor.lastrowid
        connection.commit()

        return process_action_property

    def update(self, process_action_property):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = dict()
        params['value'] = process_action_property['value']
        params['pan_id'] = process_action_property['pan_id']
        params['name'] = process_action_property['name']

        statement = "update processes_actions_properties set value = :value where pan_id = :pan_id and name = :name"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        connection.commit()

    def get_property(self, process_action, name, default_value=None):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = dict()
        params['pan_id'] = process_action['id']
        params['name'] = name

        statement = "select value from processes_actions_properties where pan_id = :pan_id and name = :name"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)

        # if the default_value holds a value, than return this values if no value is found.
        if len(result) == 0:
            if default_value:
                return default_value
            return None

        return result[0]['value']

    def set_property(self, process_action, name, value):
        params = dict()
        params['pan_id'] = process_action['id']
        params['name'] = name
        params['value'] = value

        if self.get_property(process_action, name):
            self.update(params)
        else:
            self.insert(params)
            
    def clean(self, days):
        connection = self.get_connection()
        cursor = connection.cursor()

        statement = "delete from processes_actions_properties where created_at <:created_at"

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

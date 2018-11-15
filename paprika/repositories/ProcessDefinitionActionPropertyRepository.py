from paprika.repositories.Repository import Repository
from paprika.connectors.Helper import Helper


class ProcessDefinitionActionPropertyRepository(Repository):
    def __init__(self, connector):
        Repository.__init__(self, connector)

    def list_by_process_definition_action(self, process_definition_action):
        connection = self.get_connection()
        cursor = connection.cursor()

        param = dict()
        param['dan_id'] = process_definition_action['id']

        statement = "select * from process_definitions_actions_properties where active=1 and dan_id = :dan_id"
        statement, parameters = self.statement(statement, param)

        cursor.execute(statement, parameters)

        return Helper.cursor_to_json(cursor)

    def get_property(self, process_definition_action, name):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = dict()
        params['dan_id'] = process_definition_action['id']
        params['name'] = name

        statement = "select value from process_definitions_actions_properties where dan_id = :dan_id and name = :name"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)

        if len(result) == 0:
            return None
        return result[0]['value']

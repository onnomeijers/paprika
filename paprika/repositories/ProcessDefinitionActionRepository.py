from paprika.repositories.Repository import Repository
from paprika_connector.connectors.Helper import Helper


class ProcessDefinitionActionRepository(Repository):
    def __init__(self, connector):
        Repository.__init__(self, connector)

    def list_by_process_definition(self, process_definition):
        connection = self.get_connection()
        cursor = connection.cursor()

        param = dict()
        param['pdn_id'] = process_definition['id']

        statement = "select * from process_definitions_actions where active=1 and pdn_id = :pdn_id"
        statement, parameters = self.statement(statement, param)

        cursor.execute(statement, parameters)

        return Helper.cursor_to_json(cursor)

    def find_first_by_process_definition(self, process_definition):
        connection = self.get_connection()
        cursor = connection.cursor()

        param = dict()
        param['pdn_id'] = process_definition['id']

        statement = "select * from process_definitions_actions where pdn_id = :pdn_id and active=1 order by id"
        statement, parameters = self.statement(statement, param)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)

        if len(result) == 0:
            return None
        return result[0]

    def find_next_by_process_action(self, process_action, process):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = dict()
        params['dan_id'] = process_action['dan_id']
        params['pdn_id'] = process['pdn_id']

        statement = "select * from process_definitions_actions pan where pan.id > :dan_id and pan.pdn_id = :pdn_id " \
                    "and pan.active=1 order by pan.id"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)

        if len(result) == 0:
            return None
        return result[0]
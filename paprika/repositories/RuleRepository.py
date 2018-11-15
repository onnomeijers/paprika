from paprika.repositories.Repository import Repository
from paprika.connectors.Helper import Helper


class RuleRepository(Repository):
    def __init__(self, connector):
        Repository.__init__(self, connector)

    def insert(self, message):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = dict()
        params['lcn_id'] = message.get('lcn_id')
        params['hok_id'] = message.get('hok_id')
        params['stm_id'] = message.get('stm_id')
        params['set_id'] = message.get('set_id')
        params['rule'] = message.get('rule')
        params['pattern'] = message.get('pattern')
        params['pdn_id'] = message.get('pdn_id')
        params['e_pdn_id'] = message.get('e_pdn_id')

        statement = "insert into rules(lcn_id, hok_id, stm_id, set_id, rule, pattern, pdn_id, e_pdn_id) values (:lcn_id, :hok_id, :stm_id, :set_id, :rule, :pattern, :pdn_id, :e_pdn_id)"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        message['id'] = cursor.lastrowid
        connection.commit()

        return message

    def find_by_location(self, location):
        connection = self.get_connection()
        cursor = connection.cursor()

        param = dict()
        param['lcn_id'] = location['id']

        statement = "select * from rules where active = 1 and lcn_id = :lcn_id"
        statement, parameters = self.statement(statement, param)

        cursor.execute(statement, parameters)

        return Helper.cursor_to_json(cursor)

    def find_by_hook(self, hook):
        #als er meer dan 1 id kan worden verwacht dient hiervoor list_by.... te worden gebruikt.
        connection = self.get_connection()
        cursor = connection.cursor()

        param = dict()
        param['hok_id'] = hook['id']

        statement = "select * from rules where active = 1 and hok_id= :hok_id"
        statement, parameters = self.statement(statement, param)

        cursor.execute(statement, parameters)

        return Helper.cursor_to_json(cursor)

    def list_by_scheduled_event(self, scheduled_event):
        connection = self.get_connection()
        cursor = connection.cursor()

        param = dict()
        param['set_id'] = scheduled_event['id']

        print 'scheduled_event is: ', scheduled_event
        statement = "select * from rules where active = 1 and set_id= :set_id"
        statement, parameters = self.statement(statement, param)

        cursor.execute(statement, parameters)

        return Helper.cursor_to_json(cursor)

    def find_by_stream(self, stream):
        connection = self.get_connection()
        cursor = connection.cursor()

        param = dict()
        param['stm_id'] = stream['id']

        statement = "select * from rules where active=1 and stm_id = :stm_id"
        statement, parameters = self.statement(statement, param)

        cursor.execute(statement, parameters)

        return Helper.cursor_to_json(cursor)

    def find_by_name(self, name):
        connection = self.get_connection()
        cursor = connection.cursor()

        param = dict()
        param['name'] = name

        statement = "select * from rules where name = :name"
        statement, parameters = self.statement(statement, param)

        cursor.execute(statement, parameters)

        return Helper.cursor_to_json(cursor)

    def find_failsafe(self):
        connection = self.get_connection()
        cursor = connection.cursor()

        statement = "select * from rules where active=1 and rule='failsafe'"

        cursor.execute(statement)
        result = Helper.cursor_to_json(cursor)

        if len(result) == 0:
            return None
        return result[0]

    def list(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("select * from rules where active=1")

        return Helper.cursor_to_json(cursor)

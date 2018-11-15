from paprika.repositories.Repository import Repository
from paprika.connectors.Helper import Helper


class EventRepository(Repository):
    def __init__(self, connector):
        Repository.__init__(self, connector)

    def insert(self, event):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = dict()
        params['job_name'] = event['job_name']
        params['state'] = event['state']
        params['repetition'] = event['repetition']
        params['intermission'] = event['intermission']
        params['pcs_id'] = event['pcs_id']

        statement = "insert into events(job_name, state, repetition, intermission, pcs_id) " \
                    "values (:job_name, :state, :repetition, :intermission, :pcs_id)"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        event['id'] = cursor.lastrowid
        connection.commit()

        return event

    def get_by_hashcode(self, hashcode):
        connection = self.get_connection()
        cursor = connection.cursor()

        param = dict()
        param['hashcode'] = hashcode

        statement = "select * from events where hashcode = :hashcode"
        statement, parameters = self.statement(statement, param)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)

        if len(result) == 0:
            return None
        return result[0]

    def find_by_id(self, id):
        connection = self.get_connection()
        cursor = connection.cursor()

        param = dict()
        param['id'] = id

        statement = "select * from events where id = :id"
        statement, parameters = self.statement(statement, param)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)

        if len(result) == 0:
            return None
        return result[0]

    def list(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("select * from events")

        return Helper.cursor_to_json(cursor)

    def state(self, message):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = dict()
        params['state'] = message['state']
        params['message'] = message['message']
        params['backtrace'] = message['backtrace']
        params['hashcode'] = message['hashcode']

        statement = "update events set state = :state, message = :message, backtrace = :backtrace " \
                    "where hashcode = :hashcode"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        connection.commit()

    def find_by_state(self, state):
        connection = self.get_connection()
        cursor = connection.cursor()

        param = dict()
        param['state'] = state

        statement = "select * from events where state = :state"
        statement, parameters = self.statement(statement, param)

        cursor.execute(statement, parameters)

        return Helper.cursor_to_json(cursor)

    def states(self):
        connection = self.get_connection()
        cursor = connection.cursor()

        statement = "select state, count(0) as aantal from events group by state"

        cursor.execute(statement)

        return Helper.cursor_to_json(cursor)

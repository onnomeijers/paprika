from paprika.repositories.Repository import Repository
from paprika.connectors.Helper import Helper


class ScheduledEventRepository(Repository):

    def __init__(self, connector):
        Repository.__init__(self, connector)

    def insert(self, scheduled_event):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = dict()
        params['name'] = scheduled_event['name']
        params['repetition'] = scheduled_event['repetition']
        params['intermission'] = scheduled_event['intermission']
        params['expected'] = scheduled_event['expected']
        params['active'] = scheduled_event['active']

        statement = "insert into scheduled_events(name, repetition, intermission, expected, active) " \
                    "values (:name, :repetition, :intermission, :expected, :active)"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        scheduled_event['id'] = cursor.lastrowid
        connection.commit()

        return scheduled_event

    def expected(self, scheduled_event):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = dict()
        params['expected'] = scheduled_event['expected']
        params['id'] = scheduled_event['id']

        statement = "update scheduled_events set expected = :expected where id = :id"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        connection.commit()

    def list_active(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("select * from scheduled_events where active=1")

        return Helper.cursor_to_json(cursor)

    def list(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("select * from scheduled_events")

        return Helper.cursor_to_json(cursor)

    def update(self, scheduled_event):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = dict()
        params['repetition'] = scheduled_event['repetition']
        params['intermission'] = scheduled_event['intermission']
        params['url'] = scheduled_event['url']
        params['expected'] = scheduled_event['expected']
        params['datasource'] = scheduled_event['datasource']
        params['hashcode'] = scheduled_event['hashcode']

        statement = "update scheduled_events " \
                    "set repetition = :repetition, intermission = :intermission, url = :url, expected = :expected," \
                    " datasource = :datasource, db_call = :db_call where hashcode = :hashcode"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        connection.commit()

    def hold(self, scheduled_event):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = dict()
        params['active'] = scheduled_event['active']
        params['id'] = scheduled_event['id']

        statement = "update scheduled_events set active = :active where id = :id"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        connection.commit()

    def delete(self, scheduled_event):
        connection = self.get_connection()
        cursor = connection.cursor()

        param = dict()
        param['id'] = scheduled_event['id']

        statement = "delete from scheduled_events where id = :id"
        statement, parameters = self.statement(statement, param)

        cursor.execute(statement, parameters)
        connection.commit()

    def find_by_hashcode(self, hashcode):
        connection = self.get_connection()
        cursor = connection.cursor()

        param = dict()
        param['hashcode'] = hashcode

        statement = "select * from scheduled_events where hashcode = :hashcode"
        statement, parameters = self.statement(statement, param)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)
        cursor.close()

        if len(result) == 0:
            return None
        return result[0]

    def find_by_id(self, id):
        connection = self.get_connection()
        cursor = connection.cursor()

        param = dict()
        param['id'] = id

        statement = "select * from scheduled_events where id = :id"
        statement, parameters = self.statement(statement, param)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)
        cursor.close()

        if len(result) == 0:
            return None
        return result[0]

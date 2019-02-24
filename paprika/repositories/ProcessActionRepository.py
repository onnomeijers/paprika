from paprika.repositories.Repository import Repository
from paprika_connector.connectors.Helper import Helper


class ProcessActionRepository(Repository):
    def __init__(self, connector):
        Repository.__init__(self, connector)

    def insert(self, process_action):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = dict()
        params['job_name'] = process_action['job_name']
        params['pcs_id'] = process_action['pcs_id']
        params['dan_id'] = process_action['dan_id']
        params['name'] = process_action['name']
        params['state'] = process_action['state']

        statement = "insert into processes_actions(job_name, pcs_id, dan_id, name, state) values (:job_name, :pcs_id," \
                    ":dan_id, :name, :state)"
        statement, parameters = self.statement(statement, params)
        cursor.execute(statement, parameters)
        process_action["id"] = cursor.lastrowid
        connection.commit()

        return process_action

    def find_by_id(self, id):
        connection = self.get_connection()
        cursor = connection.cursor()

        param = dict()
        param['id'] = id

        statement = "select * from processes_actions where id = :id"
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

        statement = "select * from processes_actions where hashcode = :hashcode"
        statement, parameters = self.statement(statement, param)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)

        if len(result) == 0:
            return None
        return result[0]

    def state(self, process_action):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = dict()
        params['state'] = process_action['state']
        params['message'] = process_action['message']
        params['backtrace'] = process_action['backtrace']
        params['id'] = process_action['id']

        statement = "update processes_actions set state = :state, message = :message, backtrace = :backtrace " \
                    "where id = :id"

        statement, parameters = self.statement(statement, params)
        cursor.execute(statement, parameters)
        connection.commit()

    def count_processed_by_name(self, name):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = dict()
        params['name'] = name

        statement = "select count(0) aantal from processes_actions where name=:name and state='PROCESSED'"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)

        if len(result) == 0:
            return None
        return result[0]



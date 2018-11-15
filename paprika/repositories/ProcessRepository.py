from paprika.repositories.Repository import Repository
from paprika.connectors.Helper import Helper


class ProcessRepository(Repository):
    def __init__(self, connector):
        Repository.__init__(self, connector)

    def insert(self, process):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = dict()
        params['job_name'] = process['job_name']
        params['pdn_id'] = process['pdn_id']
        params['state'] = process['state']
        params['e_pdn_id'] = process['e_pdn_id']
        params['name'] = process['name']
        params['queue'] = process['queue']

        statement = "insert into processes(job_name, pdn_id, state, e_pdn_id, name, queue) " \
                    "values (:job_name, :pdn_id, :state, :e_pdn_id, :name, :queue)"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        process["id"] = cursor.lastrowid
        connection.commit()

        return process

    def find_by_id(self, id):
        connection = self.get_connection()
        cursor = connection.cursor()

        param = dict()
        param['id'] = id

        statement = "select * from processes where id = :id"
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

        statement = "select * from processes where hashcode = :hashcode"
        statement, parameters = self.statement(statement, param)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)

        if len(result) == 0:
            return None
        return result[0]

    def find_by_name(self, name):
        connection = self.get_connection()
        cursor = connection.cursor()

        param = dict()
        param['name'] = name

        statement = "select * from processes where name = :name"
        statement, parameters = self.statement(statement, param)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)

        if len(result) == 0:
            return None
        return result[0]

    def state(self, process):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = dict()
        params['state'] = process['state']
        params['message'] = process['message']
        params['backtrace'] = process['backtrace']
        params['id'] = process['id']

        statement = "update processes set state = :state, message = :message, backtrace = :backtrace where id = :id"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        connection.commit()

    def list(self):
        connection = self.get_connection()
        cursor = connection.cursor()

        statement = "select * from processes order by id desc"
        cursor.execute(statement)
        result = Helper.cursor_to_json(cursor)

        if len(result) == 0:
            return []
        return result
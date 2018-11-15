from paprika.repositories.Repository import Repository
from paprika.connectors.Helper import Helper
from datetime import datetime
from datetime import timedelta


class ChunkRepository(Repository):
    def __init__(self, connector):
        Repository.__init__(self, connector)

    def insert(self, chunk):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = dict()
        params['job_name'] = chunk['job_name']
        params['pcs_id'] = chunk['pcs_id']
        params['state'] = chunk['state']
        params['datasource'] = chunk['datasource']
        params['tablename'] = chunk['tablename']
        params['selector'] = chunk['selector']
        params['payload'] = chunk['payload']
        params['rle_id'] = chunk['rle_id']
        params['rule'] = chunk['rule']
        params['pattern'] = chunk['pattern']
        params['options'] = chunk['options']
        params['updater'] = chunk['updater']

        statement = "insert into chunks(job_name, pcs_id, state, datasource, tablename, selector,payload, rle_id," \
                    " rule, pattern, options, updater) values (:job_name, :pcs_id, :state, :datasource, :tablename," \
                    " :selector, :payload, :rle_id, :rule, :pattern, :options, :updater)"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        chunk['id'] = cursor.lastrowid
        connection.commit()

        return chunk

    def find_by_id(self, id):
        connection = self.get_connection()
        cursor = connection.cursor()

        param = dict()
        param['id'] = id

        statement = "select * from chunks where id = :id"
        statement, parameters = self.statement(statement, param)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)

        if len(result) == 0:
            return None
        return result[0]

    def state(self, message):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = dict()
        params['state'] = message['state']
        params['message'] = message['message']
        params['backtrace'] = message['backtrace']
        params['hashcode'] = message['hashcode']

        statement = "update chunks set state = :state, message = :message, backtrace = :backtrace " \
                    "where hashcode = :hashcode"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        connection.commit()
        
    def clean(self, days):
        connection = self.get_connection()
        cursor = connection.cursor()

        statement = "delete from chunks where created_at <:created_at"

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

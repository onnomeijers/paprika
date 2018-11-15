from datetime import datetime
from datetime import timedelta
from paprika.repositories.Repository import Repository


class LogRepository(Repository):
    def __init__(self, connector):
        Repository.__init__(self, connector)

    def insert(self, log):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = dict()
        params['logtype_code'] = log['logtype_code']
        params['job_name'] = log['job_name']
        params['package_name'] = log['package_name']
        params['method_name'] = log['method_name']
        params['message'] = log['message']
        params['backtrace'] = log['backtrace']

        statement = "insert into log(logtype_code, job_name, package_name, method_name, message, format_error_backtrace)" \
                    " values (:logtype_code, :job_name, :package_name, :method_name, :message, :backtrace)"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        log['id'] = cursor.lastrowid
        connection.commit()
        cursor.close()

        return log

    def clean(self, days):
        connection = self.get_connection()
        cursor = connection.cursor()

        statement = "delete from log where created_at <:created_at"

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

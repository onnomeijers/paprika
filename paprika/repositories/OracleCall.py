from paprika.repositories.Repository import Repository
import cx_Oracle


class OracleCall(Repository):
    def __init__(self, connector):
        Repository.__init__(self, connector)

    def execute(self, call):
        connection = self.get_connection()
        cursor = connection.cursor()
        params = call['params']

        for key in params.keys():
            if str(params[key]).startswith('<<'):
                 params[key] = cursor.var(cx_Oracle.STRING)

        cursor.callproc(call['method_name'], keywordParameters=params)
        for key in params.keys():
            if type(params[key]) == cx_Oracle.STRING:
                params[key] = str(params[key].getvalue())
        cursor.close()
        connection.commit()

from paprika.repositories.Repository import Repository
from paprika.connectors.Helper import Helper
from paprika.system.logger.Logger import Logger
from paprika.connectors.ConnectorFactory import ConnectorFactory
from paprika.connectors.DatasourceBuilder import DatasourceBuilder


class OracleScheduler(Repository):
    def __init__(self, connector):
        Repository.__init__(self, connector)
        self.__logger = Logger(ConnectorFactory.create_connector(DatasourceBuilder.build('paprika-ds.json')), self)

    def get_logger(self):
        return self.__logger

    def job_run_details(self, identifier, created_at):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = dict()
        params['identifier'] = identifier
        params['created_at'] = created_at

        statement = "select status, additional_info from user_scheduler_job_run_details " \
                    "where job_name=upper(:identifier) " \
                    "and log_date>=to_timestamp_tz(:created_at,'YYYY-MM-DD HH24:MI:SS') order by log_id desc"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        results = Helper.cursor_to_json(cursor)
        cursor.close()

        if len(results) == 0:
            return None
        return results[0]

    def scheduler_jobs(self, identifier):
        connection = self.get_connection()
        cursor = connection.cursor()

        param = dict()
        param['identifier'] = identifier

        statement = "select * from user_scheduler_jobs where job_name=upper(:identifier)"
        statement, parameters = self.statement(statement, param)

        cursor.execute(statement, parameters)
        results = Helper.cursor_to_json(cursor)
        cursor.close()

        if len(results) == 0:
            return None
        return results[0]

    def is_running(self, identifier):
        scheduler_job = self.scheduler_jobs(identifier)
        if scheduler_job:
            if scheduler_job['state'] == 'RUNNING':
                return True
        return False

    def run_result(self, identifier, job_name, created_at):
        run_details = self.job_run_details(identifier, created_at)

        if run_details['status'] == 'FAILED':
            return {"state": 'FAILED', "message": run_details['additional_info'], "backtrace": ''}

        return {"state": 'SUCCEEDED', "message": '', "backtrace": ''}

    def object_type(self, job_action):
        params = dict()
        params['package'] = job_action.split('.')[0].upper()
        params['method'] = job_action.split('.')[1].upper()

        connection = self.get_connection()
        cursor = connection.cursor()

        statement = "select * from user_arguments where argument_name is null and position = 0 " \
                    "and package_name=upper(:package) and object_name=(:method)"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        count = len(Helper.cursor_to_json(cursor))

        if count == 0:
            return 'PROCEDURE'
        return 'FUNCTION'

    def action(self, message):
        params = message['params']
        test_result_params = message.get('test_result_params')
        object_type = self.object_type(message['method_name'])
        declarations = 'declare '
        returns = ''
        logger = self.get_logger()

        if object_type == 'FUNCTION':
            declarations = declarations + "l_resultaat  varchar2(4000);"  # gaat alleen goed met integers en strings
            returns = returns + "l_resultaat := "

        arguments = []
        if params:
            for argument in params:
                if str(params[argument]) == '<<':
                    declarations = declarations + argument + "  varchar2(4000);"
                    arguments.append(argument + " => " + argument)
                else:
                    arguments.append(argument + " => '" + params[argument] + "'")

        action = declarations + 'begin ' + returns + message['method_name'] + '(' + ",".join(arguments) + ');'

        if test_result_params:
            for param in test_result_params:
                test_string = param + ' in ('
                for arg in test_result_params[param]:
                    test_string += "'" + arg + "'" + ','
                test_string = test_string.rstrip(',') + ')'
                test_string += ' AND'
            test_string = test_string.rstrip('AND')

            action += ' if not(' + test_string + ") then raise_application_error( -20001, 'Error: not " + test_string.replace("'", "") + "' ); end if;"

        action += ' end;'

        logger.debug(message['identifier'], 'plsql_block := ' + action)
        return action

    def create_job(self, message):
        connection = self.get_connection()
        cursor = connection.cursor()

        arguments = dict()
        arguments['job_name'] = message['identifier']
        arguments['job_type'] = 'PLSQL_BLOCK'
        arguments['job_action'] = self.action(message)
        arguments['enabled'] = True

        cursor.callproc('dbms_scheduler.create_job', keywordParameters=arguments)
        cursor.close()

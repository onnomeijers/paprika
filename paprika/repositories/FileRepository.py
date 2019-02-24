from paprika_connector.connectors.Helper import Helper
from paprika.repositories.Repository import Repository
from paprika.system.logger.Logger import Logger
from paprika.repositories.FilePropertyRepository import FilePropertyRepository


class FileRepository(Repository):
    def __init__(self, connector):
        Repository.__init__(self, connector)
        self.__logger = Logger(connector, self)

    def get_logger(self):
        return self.__logger

    def insert(self, file):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = dict()
        params['pcs_id'] = file['pcs_id']
        params['job_name'] = file['job_name']
        params['filename'] = file['filename']
        params['state'] = file['state']
        params['rule'] = file['rule']
        params['hashcode'] = file['hashcode']
        params['pickup_location'] = file['pickup_location']
        params['path'] = file['path']
        params['filesize'] = file['filesize']
        params['pattern'] = file['pattern']
        params['rle_id'] = file['rle_id']

        statement = "insert into files(pcs_id, job_name, filename, state, rule, hashcode, pickup_location, path," \
                    " filesize, pattern, rle_id) values (:pcs_id, :job_name, :filename, :state, :rule, :hashcode," \
                    ":pickup_location, :path, :filesize, :pattern, :rle_id)"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        file['id'] = cursor.lastrowid
        connection.commit()

        return file

    def get_by_hashcode(self, hashcode):
        connection = self.get_connection()
        cursor = connection.cursor()

        param = dict()
        param['hashcode'] = hashcode

        statement = "select * from files where hashcode = :hashcode"
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

        statement = "select * from files where id = :id"
        statement, parameters = self.statement(statement, param)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)

        if len(result) == 0:
            return None
        return result[0]

    def list(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("select * from files")

        return Helper.cursor_to_json(cursor)

    def find_by_state(self, state):
        connection = self.get_connection()
        cursor = connection.cursor()

        param = dict()
        param['state'] = state

        statement = "select * from files where state = :state"
        statement, parameters = self.statement(statement, param)

        cursor.execute(statement, parameters)

        return Helper.cursor_to_json(cursor)

    def list_by_rule(self, rule):
        connection = self.get_connection()
        cursor = connection.cursor()

        param = dict()
        param['rle_id'] = rule['id']

        statement = "select * from files where rle_id = :rle_id order by id"
        statement, parameters = self.statement(statement, param)

        cursor.execute(statement, parameters)

        return Helper.cursor_to_json(cursor)

    def list_by_rule_name(self, rule_name):
        connection = self.get_connection()
        cursor = connection.cursor()

        param = dict()
        param['rule_name'] = rule_name

        statement = "select * from files where rule= :rule_name order by id"
        statement, parameters = self.statement(statement, param)

        cursor.execute(statement, parameters)

        return Helper.cursor_to_json(cursor)

    def free(self, rule_name):
        logger = self.get_logger()
        logger.trace('', 'rule : ' + rule_name)

        connection = self.get_connection()
        cursor = connection.cursor()

        param = dict()
        param['rule_name'] = rule_name

        statement = "select count(0) as aantal from files where rule = :rule_name " \
                    "and state in ('SCHEDULED','PROCESSING','READY')"
        logger.trace('', 'statement : ' + statement)
        statement, parameters = self.statement(statement, param)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)
        logger.trace('', 'aantal : ' + result[0]['aantal'])

        if int(result[0]['aantal']) == 0:
            return True
        return False

    def locked(self, file):
        logger = self.get_logger()
        logger.trace('', 'rule : ' + file['rule'])

        connection = self.get_connection()
        cursor = connection.cursor()

        file_property_repository = FilePropertyRepository(self.get_connector())
        pattern_value = file_property_repository.get_property(file, 'pattern')

        params = dict()
        params['name'] = 'pattern'
        params['value'] = pattern_value

        statement = "select f.id " \
                    "from files f " \
                    "inner join file_properties fp on f.id = fp.fle_id " \
                    "where fp.name = :name and fp.value = :value and f.state = 'WAIT' order by f.id"
        logger.trace('', 'statement : ' + statement)
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)

        if result:
            logger.trace('', 'id : ' + result[0]['id'])
            logger.trace('', 'locked : ' + str(int(result[0]['id']) != int(file['id'])))
            if int(result[0]['id']) != int(file['id']):
                return True

        statement = "select count(0) as aantal " \
                    "from files f " \
                    "inner join file_properties fp on f.id = fp.fle_id " \
                    "where fp.name = :name and fp.value = :value and f.state = 'SCHEDULED'"
        logger.trace('', 'statement : ' + statement)
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)
        logger.trace('', 'count : ' + result[0]['aantal'])

        if int(result[0]['aantal']) == 0:
            logger.trace('', 'file: ' + file['filename'] + ' not locked')
            return False
        return True

    def find_by_pickup_location(self, pickup_location):
        connection = self.get_connection()
        cursor = connection.cursor()

        param = dict()
        param['pickup_location'] = pickup_location

        statement = "select * from files where pickup_location = :pickup_location"
        statement, parameters = self.statement(statement, param)

        cursor.execute(statement, parameters)

        return Helper.cursor_to_json(cursor)

    def list_rules_by_state(self, state):
        connection = self.get_connection()
        cursor = connection.cursor()

        param = dict()
        param['state'] = state

        statement = "select distinct rule from files where state = :state"
        statement, parameters = self.statement(statement, param)

        cursor.execute(statement, parameters)

        return Helper.cursor_to_json(cursor)

    def state(self, file):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = dict()
        params['state'] = file['state']
        params['message'] = file['message']
        params['backtrace'] = file['backtrace']
        params['hashcode'] = file['hashcode']

        statement = "update files set state = :state, message = :message, backtrace = :backtrace " \
                    "where hashcode = :hashcode"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        connection.commit()

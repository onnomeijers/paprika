import MySQLdb

from paprika.system.Strings import Strings


class MysqlConnector:

    def __init__(self, datasource):
        self.__host = datasource['host']
        self.__username = datasource['username']
        self.__password = datasource['password']
        self.__database = datasource['db']
        self.__datasource = datasource
        self.__connection = self.connect()

    def get_datasource(self):
        return self.__datasource

    def get_host(self):
        return self.__host

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def get_database(self):
        return self.__database

    def get_connection(self):
        return self.__connection

    def is_connected(self):
        connection = self.get_connection()
        if connection:
            if connection.open:
                return True
        return False

    def statement(self, statement, message):
        p = []
        s = statement

        keywords = Strings.keywords(s, ':')
        for keyword in keywords:
            s = s.replace(':' + keyword, '%s')
            p.append(message[keyword])

        return s, tuple(p)

    def connect(self):
        host = self.get_host()
        username = self.get_username()
        password = self.get_password()
        database = self.get_database()
        return MySQLdb.connect(host, username, password, database)

    def close(self):
        connection = self.get_connection()
        if connection:
            if connection.open:
                connection.close()

import hashlib
from paprika_connector.connectors.Helper import Helper
from paprika.repositories.Repository import Repository
from paprika.repositories.SessionRepository import SessionRepository


class UserRepository(Repository):
    def __init__(self, connector):
        Repository.__init__(self, connector)

    def find_by_id(self, id):
        connection = self.get_connection()
        cursor = connection.cursor()

        param = dict()
        param['id'] = id

        statement = "select * from users where id = :id"
        statement, parameters = self.statement(statement, param)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)

        cursor.close()
        if len(result) == 0:
            return None
        return result[0]

    def find_by_username(self, username):
        connection = self.get_connection()
        cursor = connection.cursor()

        param = dict()
        param['username'] = username

        statement = "select * from users where username = :username"
        statement, parameters = self.statement(statement, param)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)
        cursor.close()

        if len(result) == 0:
            return None
        return result[0]

    def insert(self, user):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = dict()
        params['username'] = user['username']
        params['password'] = user['password']

        statement = "insert into users(username, password) values (:username, :password)"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        user['id'] = cursor.lastrowid
        connection.commit()

        return user

    def update(self, user):
        connection = self.get_connection()
        cursor = connection.cursor()

        param = dict()
        param['name'] = user['name']
        param['nickname'] = user['nickname']
        param['hashcode'] = user['hashcode']

        statement = "update users set name=:name, nickname=:nickname where hashcode=:hashcode"
        statement, parameters = self.statement(statement, param)

        cursor.execute(statement, parameters)
        connection.commit()

        return user

    def register(self, username, password):
        user = self.find_by_username(username)
        if not user:
            self.insert({"username": username, "password": password})

    def login(self, username, password):
        user = self.find_by_username(username)

        md5 = hashlib.md5()
        md5.update(password)

        if user:
            if user['password'] == md5.hexdigest():
                session_repository = SessionRepository(self.get_connector())
                session = session_repository.create()
                session = session_repository.find_by_id(session['id'])
                return session['hashcode']
        return None

    def list(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("select * from users")

        return Helper.cursor_to_json(cursor)

    def find_by_hashcode(self, hashcode):
        connection = self.get_connection()
        cursor = connection.cursor()
        param = dict()
        param['hashcode'] = hashcode
        statement = "select * from users where hashcode = :hashcode"
        statement, parameters = self.statement(statement, param)
        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)
        cursor.close()

        if len(result) == 0:
            return None
        return result[0]

from paprika.connectors.Helper import Helper
from paprika.repositories.Repository import Repository
from paprika.system.Ora import Ora
from datetime import datetime
from datetime import timedelta


class MessageException(Exception):
    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return repr(self.__message)

    def get_message(self):
        return self.__message


class MessageRepository(Repository):
    def __init__(self, connector):
        Repository.__init__(self, connector)

    def insert(self, queue, message):
        connection = self.get_connection()
        cursor = connection.cursor()

        tablename = queue['tablename']

        params = dict()
        params['state'] = message['state']
        params['delay'] = message['delay']
        params['payload'] = message['payload']
        params['agent'] = message['agent']
        params['consumer'] = message['consumer']

        statement = "insert into " + tablename + "(state, delay, payload, agent, consumer) " \
                                                 "values(:state, :delay, :payload, :agent, :consumer)"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        message['id'] = cursor.lastrowid
        connection.commit()

        return message

    def state(self, queue, message, state):
        connection = self.get_connection()
        cursor = connection.cursor()

        tablename = queue['tablename']

        statement = "update " + tablename + " set state=:state, message=:message, backtrace=:backtrace where id=:id"

        params = dict()
        params['state'] = state
        params['message'] = Ora.iif(message, 'message', '')
        params['backtrace'] = Ora.iif(message, 'backtrace', '')
        params['id'] = message['id']

        statement, parameters = self.statement(statement, params)
        cursor.execute(statement, parameters)
        cursor.close()
        connection.commit()

    def wait(self, queue):
        connection = self.get_connection()
        cursor = connection.cursor()

        tablename = queue['tablename']

        statement = "update " + tablename + " set state='READY' where delay <= now() and state='WAIT'"

        cursor.execute(statement)
        cursor.close()
        connection.commit()

    def next(self, queue):
        connection = self.get_connection()
        cursor = connection.cursor()

        tablename = queue['tablename']

        statement = "select * from " + tablename + " where state='READY' order by delay"
        cursor.execute(statement)
        result = Helper.cursor_to_json(cursor)

        if len(result) == 0:
            return None
        return result[0]

    def dequeue(self, claim, queue):
        try:
            claim.acquire()
            self.wait(queue)
            message = self.next(queue)

            if message:
                # set the state of the payload to PROCESSING
                self.state(queue, message, 'PROCESSING')

            claim.release()
            return message
        except:
            claim.release()
            raise MessageException("dequeue failed.")
        
    def clean(self, days):
        connection = self.get_connection()
        cursor = connection.cursor()

        statement = "delete from messages where created_at <:created_at"

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

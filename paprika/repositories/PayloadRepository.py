from paprika.repositories.Repository import Repository
from paprika_connector.connectors.Helper import Helper
from paprika.system.ExpressionParser import ExpressionParser
from paprika.system.JsonExt import JsonExt


class PayloadException(Exception):
    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return repr(self.__message)

    def get_message(self):
        return self.__message


class PayloadRepository(Repository):
    def __init__(self, connector):
        Repository.__init__(self, connector)

    def next(self, hook):
        connection = self.get_connection()
        cursor = connection.cursor()

        statement = hook['selector']
        cursor.execute(statement)

        payload = Helper.cursor_to_json(cursor)
        cursor.close()

        if len(payload) == 0:
            return None
        return payload[0]

    def state(self, hook, payload, state):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = dict()
        # maps the given expressions in options to params.
        options = JsonExt.loads(hook['options'])
        if options:
            options = ExpressionParser.parse(options, locals())
            for key in options.keys():
                params[key] = options[key]

        statement = hook['updater']
        statement, parameters = self.statement(statement, params)
        cursor.execute(statement, parameters)
        cursor.close()
        connection.commit()

    def dequeue(self, claim, hook):
        payload = None
        try:
            claim.acquire()
            payload = self.next(hook)
            if payload:
                # set the state of the payload to PROCESSING
                self.state(hook, payload, 'READY')
        finally:
            claim.release()
            return payload

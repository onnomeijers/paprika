from paprika.repositories.Repository import Repository
from paprika.connectors.Helper import Helper


class HookRepository(Repository):
    def __init__(self, connector):
        Repository.__init__(self, connector)

    def list_active(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("select * from hooks where active=1")

        return Helper.cursor_to_json(cursor)

    def list(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("select * from hooks")

        return Helper.cursor_to_json(cursor)

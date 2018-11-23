from paprika.repositories.Repository import Repository


class OracleInsert(Repository):
    def __init__(self, connector):
        Repository.__init__(self, connector)

    def execute(self, statement, params):
        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.executemany(statement, keywordParameters=params)
        cursor.close()
        connection.commit()

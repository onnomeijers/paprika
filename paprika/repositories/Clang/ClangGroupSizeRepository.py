from paprika.repositories.Repository import Repository
from paprika_connector.connectors.Helper import Helper


class ClangGroupSizeRepository(Repository):
    def __init__(self, connector):
        Repository.__init__(self, connector)

    def insert(self, message):
        connection = self.get_connection()
        cursor = connection.cursor()
        statement = Helper.statement("insert into clang_group_sizes(customer_count, customer_count_recursive,name) values ({},{},{})"
                                     , message['customer_count']
                                     , message['customer_count_recursive']
                                     , message['name'])
        cursor.execute(statement)
        if self.has_lastrowid():
            message['id'] = cursor.lastrowid
        connection.commit()
        return message

    def clean(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        statement = "delete from clang_group_sizes"
        print statement
        cursor.execute(statement)
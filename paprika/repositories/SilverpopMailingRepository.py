from paprika.repositories.Repository import Repository


class SilverpopMailingRepository(Repository):
    def __init__(self, connector):
        Repository.__init__(self, connector)

    def insert(self, silverpop_mailing):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = dict()
        params['mailing_id'] = silverpop_mailing['mailing_id']
        params['mailing_name'] = silverpop_mailing['mailing_name']

        statement = "insert into silverpop_mailings(mailing_id, mailing_name) values (:mailing_id, :mailing_name)"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)

        if self.has_lastrowid():
            silverpop_mailing['id'] = cursor.lastrowid
        connection.commit()

        return silverpop_mailing

    def clean(self):
        connection = self.get_connection()
        cursor = connection.cursor()

        statement = "delete from silverpop_mailings"
        cursor.execute(statement)

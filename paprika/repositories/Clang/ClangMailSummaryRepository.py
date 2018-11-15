from paprika.repositories.Repository import Repository


class ClangMailSummaryRepository(Repository):
    def __init__(self, connector):
        Repository.__init__(self, connector)

    def insert(self, message):
        connection = self.get_connection()
        cursor = connection.cursor()

        statement = "insert into clang_mail_summaries (mailing_id, received, ctr, unique_opens, ended_at, description, unique_clicks, bounces, cor,campaign_name, started_at, cto, content_name) values (:mailing_id, :received, :ctr, :unique_opens, :ended_at, :description, :unique_clicks, :bounces, :cor, :campaign_name, :started_at, :cto, :content_name)"
        statement, parameters = self.statement(statement, message)
        cursor.execute(statement, parameters)

        if self.has_lastrowid():
            message['id'] = cursor.lastrowid
        connection.commit()
        return message

    def clean(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        statement = "delete from clang_mail_summaries"
        print statement
        cursor.execute(statement)
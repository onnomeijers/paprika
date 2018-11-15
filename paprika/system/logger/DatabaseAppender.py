from paprika.repositories.LogRepository import LogRepository


class DatabaseAppender:
    def __init__(self, connector):
        self.__connector = connector

    def get_connector(self):
        return self.__connector

    def write(self, message):
        connector = self.get_connector()
        logger = LogRepository(connector)
        logger.insert(message)

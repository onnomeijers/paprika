from threading import Condition
from threading import Lock
from paprika.connectors.ConnectorFactory import ConnectorFactory


class ConnectorPool(object):
    def __init__(self, max=30):
        object.__init__(self)
        self.__connectors = []
        self.__condition = Condition(Lock())
        self.__max = max
        self.__claims = []

    def get_claims(self):
        return self.__claims

    def get_connectors(self):
        return self.__connectors

    def get_condition(self):
        return self.__condition

    def claim_connector(self, datasource):
        connectors = self.get_connectors()
        result = None
        for connector in connectors:
            if datasource == connector[0]:
                result = connector[1]
                connectors.remove(connector)
                return result

    def get_count(self, datasource):
        claims = self.get_claims()
        for claim in claims:
            if claim[0] == datasource:
                return claim[1]
        return self.__max

    def set_count(self, datasource, count):
        claims = self.get_claims()
        found = False
        for claim in claims:
            if claim[0] == datasource:
                found = True
                claim[1] = count

        if not found:
            claims.append([datasource, count])

    def claim(self, datasource):
        condition = self.get_condition()
        condition.acquire()
        count = self.get_count(datasource)

        while count == 0:
            condition.wait()

        # re-use a connector from connector list.
        # if there is no connector present create one.
        connector = self.claim_connector(datasource)
        if not connector:
            connector = ConnectorFactory.create_connector(datasource)

        count -= 1
        self.set_count(datasource, count)
        condition.release()
        return connector

    def free(self, connector):
        condition = self.get_condition()
        condition.acquire()

        connectors = self.get_connectors()
        ds = connector.get_datasource()
        connectors.append([ds, connector])

        count = self.get_count(ds)
        count += 1
        self.set_count(ds, count)

        condition.notify()
        condition.release()

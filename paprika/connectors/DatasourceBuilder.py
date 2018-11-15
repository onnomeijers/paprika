import json
import os
from paprika.repositories.DatasourceRepository import DatasourceRepository
from paprika.system.Finder import Finder
import paprika


class DatasourceBuilder:
    def __init__(self):
        pass

    @staticmethod
    def build(filename):
        properties = dict()
        properties['agent.dir'] = os.path.abspath(os.path.dirname(paprika.__file__))
        properties['current.dir'] = os.path.abspath('.')
        f = Finder.open(properties, filename)
        datasource = json.load(f)
        f.close()

        return datasource

    @staticmethod
    def find(connector, name):
        datasource_repository = DatasourceRepository(connector)
        datasource = datasource_repository.get_by_name(name)
        if not datasource:
            datasource = DatasourceBuilder.build(name + ".json")
        return datasource


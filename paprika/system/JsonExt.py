import json


class JsonExt(object):
    def __init__(self):
        pass

    @staticmethod
    def loads(s, encoding=None):
        if s:
            return json.loads(s, encoding=encoding)
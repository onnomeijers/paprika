class Matcher:
    def __init__(self):
        pass

    @staticmethod
    def match(method, pattern, value):
        return method.match(pattern, value)

import re


class ReMethod:
    def __init__(self):
        pass

    @staticmethod
    def match(pattern, value):
        p = re.compile(pattern, re.IGNORECASE)
        m = p.match(value)
        if m:
            return True
        else:
            return False

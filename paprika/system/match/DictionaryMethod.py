class DictionaryMethod:

    def __init__(self):
        pass

    @staticmethod
    def match(pattern, value):
        # if no pattern is given in the rule, it always matches.
        if not pattern:
            return True

        for p in pattern.iterkeys():
            if p not in value.keys():
                return False

            if pattern[p] != value[p]:
                return False

        return True

class DictExt:

    def __init__(self):
        pass

    @staticmethod
    def dot(key, dictionary):
        """
        Returns the value in a dict using a dot notation to point to the key.
        :param key:
        :param dictionary:
        :return:
        """
        keywords = key.split('.')
        if len(keywords) > 1:
            result = DictExt.dot(".".join(keywords[1::]), dictionary[keywords[0]])
        if len(keywords) == 1:
            return dictionary[key]
        return result

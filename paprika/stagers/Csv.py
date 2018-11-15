class Csv:
    def __init__(self):
        pass

    @staticmethod
    def to_json(line, header, delimiter):
        header_list = header.split(delimiter)
        columns = line.split(delimiter)
        result = dict()

        for i in xrange(0, len(header_list)):
            value = columns[i]
            value = value.rstrip(chr(10))
            value = "'" + value + "'"
            key = header_list[i]
            result[key] = value
        return result
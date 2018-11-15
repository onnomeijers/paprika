import codecs
import magic


class CsvFile:
    def __init__(self):
        pass

    @staticmethod
    def read_header(filename, delimiter):
        r = open(filename, 'rb')
        line = r.readline()
        line = line.rstrip(chr(10))
        r.close()
        return line

    @staticmethod
    def iconv(source_filename, source_encoding, target_filename, target_encoding):
        block_size = 1048576
        with codecs.open(source_filename, "rb", source_encoding) as source_file:
            with codecs.open(target_filename, "wb", target_encoding) as target_file:
                while True:
                    contents = source_file.read(block_size)
                    if not contents:
                        break
                    target_file.write(contents)

    @staticmethod
    def normalize(source_filename, target_filename):
        block_size = 1048576
        with open(source_filename, 'rb') as source_file:
            with open(target_filename, 'wb') as target_file:
                while True:
                    contents = source_file.read(block_size)
                    contents = contents.replace(chr(13)+chr(10), chr(10))
                    contents = contents.replace(chr(13), chr(10))
                    if not contents:
                        break
                    target_file.write(contents)

    @staticmethod
    def guess_delimiter(filename, delimiters=[';', ':', ' ', '|', '~', '#']):
        r = open(filename, 'rb')
        line = r.readline()
        r.close()
        characters = []
        for s in line:
            found = False
            for c in characters:
                if c[0] == s:
                    found = True
                c[1] += + 1
            if not found and s in delimiters:
                characters.append([s, 1])
                characters.sort(reverse=True)
        return characters[0][0]

    @staticmethod
    def guess_encoding(filename):
        m = magic.Magic(flags=magic.MAGIC_MIME_ENCODING)
        mime_type = m.id_filename(filename)
        m.close()
        return mime_type
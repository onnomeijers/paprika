import stat


class Path:
    @staticmethod
    def extension(filename):
        items = filename.split('.')
        count = len(items)
        if count > 1:
            return ".".join(items[1:])
        return ''

    @staticmethod
    def mode(st_mode):
        # for dos files
        st_mode |= 0x10
        if stat.S_ISDIR(st_mode):
            return "D"
        if st_mode == 0:
            return "D"
        return "F"


import re
import time


class Client:
    def __init__(self):
        self.__excluded_extensions = []
        self.__stable_check_delay = 60
        self.__regular_expressions = []

    def get_stable_check_delay(self):
        return self.__stable_check_delay

    def set_stable_check_delay(self, stable_check_delay):
        self.__stable_check_delay = stable_check_delay

    def get_excluded_extensions(self):
        return self.__excluded_extensions

    def set_excluded_extensions(self, excluded_extensions):
        exclusions = []
        extensions = excluded_extensions.split(';')
        for extension in extensions:
            exclusions.append(extension)
        self.__excluded_extensions = exclusions

    def is_excluded(self, message):
        excluded_extensions = self.get_excluded_extensions()
        if message['extension'] in excluded_extensions:
            return True
        return False

    def get_regular_expressions(self):
        return self.__regular_expressions

    def set_regular_expressions(self, regular_expressions):
        results = []
        if regular_expressions:
            patterns = regular_expressions.split(';')
            for pattern in patterns:
                results.append(pattern)
            self.__regular_expressions = results

    def match(self, pattern, value):
        p = re.compile(pattern, re.IGNORECASE)
        m = p.match(value)
        if m:
            return True
        else:
            return False

    def is_matched(self, message):
        patterns = self.get_regular_expressions()
        if patterns:
            for pattern in patterns:
                if self.match(pattern, message['filename']):
                    return True
            return False
        return True

    def list_stable(self, path, recursive=0, depth=-1):
        stable_check_delay = self.get_stable_check_delay()
        start_files = self.list(path, recursive, depth)
        time.sleep(stable_check_delay)
        end_files = self.list(path, recursive, depth)

        results = []
        for start_file in start_files:
            if start_file in end_files:
                results.append(start_file)
        return results

    def get_path(self):
        url = self.get_url()
        return url['path']

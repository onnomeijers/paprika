import threading


class SecondTimer(object):
    def __init__(self, seconds):
        object.__init__(self)
        self.__executors = []
        self.__seconds = seconds
        self.__elapsed = 0

    def get_elapsed(self):
        return self.__elapsed

    def set_elapsed(self, elapsed):
        self.__elapsed = elapsed

    def get_seconds(self):
        return self.__seconds

    def set_seconds(self, seconds):
        self.__seconds = seconds

    def get_executors(self):
        return self.__executors

    def on_time(self):
        elapsed = self.get_elapsed()
        elapsed += 1
        self.set_elapsed(elapsed)
        seconds = self.get_seconds()
        if elapsed % seconds == 0:
            executors = self.get_executors()
            for executor in executors:
                t = threading.Thread(target=executor.execute)
                t.setDaemon(True)
                t.start()

    def register(self, executor):
        executors = self.get_executors()
        executors.append(executor)

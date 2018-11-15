import time
from paprika.threads.Runnable import Runnable


class TimerLauncher(Runnable):
    def __init__(self):
        Runnable.__init__(self)
        self.__timers = []

    def run(self):
        while 1:
            for timer in self.__timers:
                timer.on_time()
            time.sleep(1)

    def register(self, timer):
        self.__timers.append(timer)

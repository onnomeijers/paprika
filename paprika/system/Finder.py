import os


class Finder:

    def __init__(self):
        pass

    @staticmethod
    def open(properties, filename):
        url = os.path.join(properties['current.dir'], filename)
        if os.path.isfile(url):
            return open(url)

        url = os.path.join(properties['agent.dir'], filename)
        if os.path.isfile(url):
            return open(url)

        return open(filename)

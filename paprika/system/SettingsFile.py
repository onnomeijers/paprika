import os


class SettingsFile:
    def __init__(self):
        pass

    @staticmethod
    def open(properties, filename):
        if os.path.isfile(filename):
            return open(filename)
        folder = properties['agent_dir']
        if os.path.isfile(os.path.join(folder, filename)):
            return open(os.path.join(folder, filename))

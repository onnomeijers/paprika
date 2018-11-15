from multiprocessing import Process


class Launcher:
    def __init__(self):
        pass

    @staticmethod
    def run(launcher, *args):
        p = Process(target=launcher.run, args=args, name=launcher.__class__.__name__)
        p.daemon = True
        p.start()
        return p

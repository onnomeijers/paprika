from paprika.system.Console import Console
from paprika.actions.Actionable import Actionable


class Echo(Actionable):
    def __init__(self):
        Actionable.__init__(self)

    def execute(self, connector, process_action):
        Console.write(process_action['name'])

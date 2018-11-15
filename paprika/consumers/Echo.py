import json
from paprika.consumers.Consumable import Consumable
from paprika.system.logger.Logger import Logger


class Echo(Consumable):
    def __init__(self):
        Consumable.__init__(self)

    def action(self, connector, message):
        logger = Logger(self)

        payload = json.loads(message['payload'])
        logger.info('', str(payload))

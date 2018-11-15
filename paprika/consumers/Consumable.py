from paprika.consumers.ConsumeException import ConsumeException


class Consumable(object):
    def __init__(self):
        object.__init__(self)

    def action(self, connector, message):
        raise ConsumeException("method not implemented")

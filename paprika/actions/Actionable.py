from paprika.actions.ActionException import ActionException


class Actionable(object):
    def __init__(self):
        object.__init__(self)

    def execute(self, connector, process_action):
        raise ActionException("method not implemented")

class ProtocolBuilder:
    def __init__(self):
        pass

    @staticmethod
    def build(url):
        message = dict()
        message['url'] = url
        message['protocol'] = url.split('://')[0]
        return message

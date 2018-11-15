class FileUrlBuilder:
    def __init__(self):
        pass

    @staticmethod
    def build(url):
        message = dict()
        message['url'] = url
        message['protocol'] = url.split('://')[0]
        message['path'] = '/'.join(url.split('://')[1:])
        return message

# supports file://path

class SmbUrlBuilder:
    def __init__(self):
        pass

    @staticmethod
    def build(url):
        message = dict()
        message['url'] = url
        message['protocol'] = url.split('://')[0]
        message['username'] = url.split('://')[1].split('@')[0].split(':')[0]
        message['password'] = url.split('://')[1].split('@')[0].split(':')[1]
        message['host'] = url.split('://')[1].split('@')[1].split('/')[0]
        message['share'] = url.split('://')[1].split('@')[1].split('/')[1]
        message['path'] = '/'.join(url.split('://')[1].split('@')[1].split('/')[2:])
        return message

# supports smb://username:password@host/share/path
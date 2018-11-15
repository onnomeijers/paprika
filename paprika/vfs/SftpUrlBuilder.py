class SftpUrlBuilder:
    def __init__(self):
        pass

    @staticmethod
    def build(url):
        message = dict()
        message['url'] = url
        message['protocol'] = url.split('://')[0]

        ats = url.split('://')[1].split('@')
        url_part = ats[len(ats)-1]

        user_part = "@".join(ats[0:len(ats)-1])
        message['username'] = user_part.split(":")[0]
        message['password'] = user_part.split(":")[1]

        message['host'] = url_part.split("/")[0].split(":")[0]
        message['port'] = url_part.split("/")[0].split(":")[1]
        message['path'] = '/'.join(url_part.split("/")[1:])
        return message

# supports sftp://username:password@host:port/path

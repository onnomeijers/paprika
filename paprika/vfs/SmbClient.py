from paprika.vfs.Client import Client
from paprika.vfs.Path import Path
import smbclient
import hashlib
from datetime import datetime


class SmbClient(Client):
    def __init__(self, url):
        Client.__init__(self)
        self.__url = url
        self.__client = None

    def get_url(self):
        return self.__url

    def connect(self):
        url = self.get_url()
        host = url['host']
        share = url['share']
        username = url['username']
        password = url['password']
        self.__client = smbclient.SambaClient(host, share, username=username, password=password)

    def get_client(self):
        return self.__client

    def put(self, local_path, remote_path):
        client = self.get_client()
        r = open(local_path, 'rb')
        w = client.open(remote_path, 'wb')
        stream = r.read(1024)
        while stream != "":
            w.write(stream)
            stream = r.read(1024)
        w.close()
        r.close()

    def get(self, remote_path, local_path):
        client = self.get_client()
        r = client.open(remote_path, 'rb')
        w = open(local_path, 'wb')
        stream = r.read(1024)
        while stream != "":
            w.write(stream)
            stream = r.read(1024)
        w.close()
        r.close()

    def write(self, record, remote_path, append=False, encoding='utf-8'):
        raise

    def list(self, path, recursive=0, depth=-1):
        url = self.get_url()
        client = self.get_client()
        files = client.lsdir(path)
        results = []
        for file in files:
            mode = file[1]
            if file[1] == '': mode = 'F'

            message = dict()
            message['url'] = url['url']
            message['filename'] = file[0]
            message['path'] = path
            message['extension'] = Path.extension(file[0])
            message['mode'] = mode
            message['size'] = file[2]
            message['timestamp'] = file[3].strftime("%d-%m-%Y %H:%M:%S")

            md5 = hashlib.md5()
            md5.update(message['url']+'|'+message['filename']+'|'+str(message['timestamp'])+'|'+str(message['size']))
            message['hashcode'] = md5.hexdigest()

            # only add files
            if self.is_matched(message) and not self.is_excluded(message) and message['mode'] == 'F':
                results.append(message)

            # recursive and depth support
            if recursive != 0 and message['mode'] == 'D':
                if depth > 0 or depth == -1:
                    if depth != -1:
                        depth -= 1
                    recursive_results = self.list(message['path']+'/'+message['filename'], recursive, depth)
                    for recursive_result in recursive_results:
                        results.append(recursive_result)

        results.sort(key=lambda x: datetime.strptime(x['timestamp'], '%d-%m-%Y %H:%M:%S'))
        return results

    def close(self):
        # the client has a close method, but the raises the warning
        # Exception OSError: (2, 'No such file or directory', '/tmp/smb.auth.rNPWvY') in  ignored
        pass

    def delete(self, remote_path, recursive=True):
        raise

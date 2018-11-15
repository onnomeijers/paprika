from paprika.vfs.Client import Client
from paprika.vfs.Path import Path
from datetime import datetime
import hashlib
import paramiko


class SftpClient(Client):
    def __init__(self, url):
        Client.__init__(self)
        self.__url = url
        self.__client = None
        self.__sftp = None

    def get_url(self):
        return self.__url

    def connect(self):
        url = self.get_url()
        host = url['host']
        port = int(url['port'])
        username = url['username']
        password = url['password']
        self.__client = paramiko.client.SSHClient()
        self.__client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.__client.connect(host, port=port, username=username, password=password)
        self.__sftp = self.__client.open_sftp()

    def get_client(self):
        return self.__client

    def get_sftp(self):
        return self.__sftp

    def put(self, local_path, remote_path):
        sftp = self.get_sftp()
        sftp.put(local_path, remote_path)

    def get(self, remote_path, local_path):
        sftp = self.get_sftp()
        sftp.get(remote_path, local_path)

    def write(self, record, remote_path, append=False, encoding='utf-8'):
        raise

    def list(self, path, recursive=0, depth=-1):
        url = self.get_url()
        sftp = self.get_sftp()
        attributes = sftp.listdir_attr(path)
        files = sftp.listdir(path)
        count = len(files)
        results = []
        for index in xrange(0, count):
            file = files[index]
            attribute = attributes[index]
            message = dict()
            message['url'] = url['url']
            message['filename'] = file
            message['path'] = path
            message['extension'] = Path.extension(file)
            message['mode'] = Path.mode(attribute.st_mode)
            message['size'] = attribute.st_size
            message['timestamp'] = datetime.fromtimestamp(attribute.st_mtime).strftime("%d-%m-%Y %H:%M:%S")

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
        client = self.get_client()
        client.close()

    def delete(self, remote_path):
        sftp = self.get_sftp()
        sftp.remove(remote_path)

    def delete_dir(self, remote_path):
        sftp = self.get_sftp()
        sftp.rmdir(remote_path)
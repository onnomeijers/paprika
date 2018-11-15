from paprika.vfs.Client import Client
from hdfs import InsecureClient


class HdfsClient(Client):
    def __init__(self, url):
        Client.__init__(self)
        self.__url = url
        self.__client = None

    def get_url(self):
        return self.__url

    def connect(self):
        url = self.get_url()
        host = url['host']
        port = url['port']
        username = url['username']
        self.__client = InsecureClient(url='http://'+host+':'+port, user=username)

    def get_client(self):
        return self.__client

    def put(self, local_path, remote_path):
        client = self.get_client()
        client.upload(remote_path, local_path)

    def get(self, remote_path, local_path):
        client = self.get_client()
        client.download(remote_path, local_path)

    def write(self, record, remote_path, append=False, encoding='utf-8'):
        client = self.get_client()
        client.write(remote_path, data=record, encoding=encoding, append=append)

    def list(self, path, recursive=0, depth=-1):
        client = self.get_client()
        files = client.list(path)
        return files

    def close(self):
        pass

    def delete(self, remote_path, recursive=True):
        client = self.get_client()
        client.delete(remote_path, recursive=recursive)

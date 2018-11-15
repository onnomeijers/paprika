from paprika.vfs.Client import Client
from paprika.vfs.Path import Path
from zipfile import ZipFile
from datetime import datetime
import zipfile
import hashlib


class ZipClient(Client):
    def __init__(self, url):
        Client.__init__(self)
        self.__url = url
        self.__client = None

    def get_url(self):
        return self.__url

    def get_client(self):
        return self.__client

    def connect(self, mode='r'):
        url = self.get_url()
        path = url['path']
        self.__client = ZipFile(path, mode)

    def put(self, local_path, remote_path):
        self.connect('w')
        client = self.get_client()
        client.write(local_path, remote_path, zipfile.ZIP_STORED)

    def get(self, remote_path, local_path):
        self.connect('r')
        client = self.get_client()
        r = client.open(remote_path, 'r')
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

        files = client.infolist()
        count = len(files)
        results = []
        for index in xrange(0, count):
            file = files[index]

            message = dict()
            message['url'] = url['url']
            message['filename'] = file.filename
            message['path'] = path
            message['extension'] = Path.extension(file.filename)
            message['mode'] = Path.mode(file.external_attr >> 16)
            message['size'] = file.file_size
            message['timestamp'] = datetime(*file.date_time).strftime("%d-%m-%Y %H:%M:%S")

            md5 = hashlib.md5()
            md5.update(message['url']+'|'+message['filename']+'|'+str(message['timestamp'])+'|'+str(message['size']))
            message['hashcode'] = md5.hexdigest()

            print message

            # only add files
            if self.is_matched(message) and not self.is_excluded(message) and message['mode'] == 'F':
                results.append(message)

            # # recursive and depth support
            # if recursive != 0 and message['mode'] == 'D':
            #     if depth > 0 or depth == -1:
            #         if depth != -1:
            #             depth -= 1
            #         recursive_results = self.list(message['path']+'/'+message['filename'], recursive, depth)
            #         for recursive_result in recursive_results:
            #             results.append(recursive_result)

        # sort the files on timestamp
        results.sort(key=lambda x: datetime.strptime(x['timestamp'], '%d-%m-%Y %H:%M:%S'))
        return results

    def close(self):
        client = self.get_client()
        client.close()

    def delete(self, remote_path, recursive=True):
        raise
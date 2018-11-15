from paprika.vfs.Client import Client
from paprika.vfs.Path import Path
from datetime import datetime
import hashlib
import os


class FileClient(Client):
    def __init__(self, url):
        Client.__init__(self)
        self.__url = url

    def get_url(self):
        return self.__url

    def connect(self):
        pass

    def put(self, local_path, remote_path):
        r = open(local_path, 'rb')
        w = open(remote_path, 'wb')
        stream = r.read(1024)
        while stream != "":
            w.write(stream)
            stream = r.read(1024)
        w.close()
        r.close()

    def get(self, remote_path, local_path):
        r = open(remote_path, 'rb')
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
        files = os.listdir(path)
        count = len(files)
        results = []
        for index in xrange(0, count):
            file = files[index]
            attribute = os.lstat(path+os.sep+file)

            message = dict()
            message['url'] = url['url']
            message['filename'] = file
            message['path'] = path
            message['extension'] = Path.extension(file)
            message['mode'] = Path.mode(attribute[0])
            message['size'] = attribute[6]
            message['timestamp'] = datetime.fromtimestamp(attribute[8]).strftime("%d-%m-%Y %H:%M:%S")

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
                    recursive_results = self.list(message['path']+os.sep+message['filename'], recursive, depth)
                    for recursive_result in recursive_results:
                        results.append(recursive_result)
        # sort the files on timestamp
        results.sort(key=lambda x: datetime.strptime(x['timestamp'], '%d-%m-%Y %H:%M:%S'))
        return results

    def close(self):
        pass

    def delete(self, remote_path):
        os.remove(remote_path)

    def delete_dir(self, remote_path):
        os.rmdir(remote_path)
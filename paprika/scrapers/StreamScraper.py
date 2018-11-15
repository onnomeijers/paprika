import json
import requests
from paprika.messaging.Message import Message
from paprika.system.logger.Logger import Logger


class StreamScraper:
    def __init__(self):
        pass

    @staticmethod
    def listen(connector, job_name, stream, url, auth):
        response = requests.get(url, auth=auth, stream=True)
        for line in response.iter_lines(decode_unicode=True, chunk_size=None):
            if line:
                decoded_line = line.decode('utf-8')
                payload = json.loads(decoded_line)
                payload['oxyma.stream.hashcode'] = stream['hashcode']
                Message.enqueue(connector, 'messages', payload, 'streams', 'paprika.consumers.StreamProcessor.StreamProcessor')
                logger = Logger(connector, StreamScraper())
                logger.debug(job_name, json.dumps(payload))


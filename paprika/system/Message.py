import json

from paprika.system.logger.Logger import Logger
from requests import post
from paprika.system.Traceback import Traceback


class Message:

    def __init__(self):
        pass

    @staticmethod
    def get_header(response, name):
        for key in response.headers.keys():
            if key.lower() == name:
                result = response.headers[key]
                return result

    @staticmethod
    def post_request(url, message):
        logger = Logger(Message())

        try:
            headers = {'Content-Type': 'application/json'}
            logger.debug('', 'url : ' + url + ', message : ' + json.dumps(message))
            response = post(url, json.dumps(message), headers=headers)
            content_type = Message.get_header(response, 'content-type')
            logger.debug('', 'url : ' + url + ', response : ' + str(response.status_code) + ', message : ' + json.dumps(message))
            logger.debug('', 'url : ' + url + ', content_type : ' + str(content_type) + ', message : ' + json.dumps(message))

            if content_type == 'application/json':
                result = json.loads(response.content)
                result['status_code'] = response.status_code
            else:
                result = dict()
                result['state'] = 'FAILED'
                result['status_code'] = response.status_code
                result['message'] = response.reason
                result['backtrace'] = response.text
            return result
        except:
            result = Traceback.build()
            result['state'] = 'FAILED'
            result['status_code'] = 400
            return result

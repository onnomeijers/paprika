from requests import post
import json


class RestRequest:
    def __init__(self):
        pass

    @staticmethod
    def post(headers, url, message, certificate, proxies, verify=True):

        # retrieve the file locations of the crt and key.
        cert = None
        if certificate:
            cert = (certificate['crt'], certificate['key'])

        response = post(url, json.dumps(message), headers=headers, cert=cert, proxies=proxies, verify=verify)
        return response

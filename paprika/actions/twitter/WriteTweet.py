from paprika.actions.Actionable import Actionable
from paprika.repositories.ProcessActionPropertyRepository import ProcessActionPropertyRepository
from paprika.repositories.ProcessPropertyRepository import ProcessPropertyRepository
from paprika.repositories.ProcessRepository import ProcessRepository
from paprika.system.logger.Logger import Logger
from paprika.services.RestRequest import RestRequest
from paprika.actions.ProcessException import ProcessException
from paprika.system.ExpressionParser import ExpressionParser
import json
from paprika.system.JsonExt import JsonExt


class WriteTweet(Actionable):
    def __init__(self):
        Actionable.__init__(self)

    def execute(self, connector, process_action):
        logger = Logger(connector, self)
        job_name = process_action['job_name']

        process_repository = ProcessRepository(connector)
        process_property_repository = ProcessPropertyRepository(connector)
        process_action_property_repository = ProcessActionPropertyRepository(connector)
        # retrieve the file properties
        process = process_repository.find_by_id(process_action['pcs_id'])

        # retrieve the payload if present
        payload = JsonExt.loads(process_property_repository.get_property(process, 'payload'))

        twitter_token = process_action_property_repository.get_property(process_action, 'twitter_token')
        twitter_token = JsonExt.loads(twitter_token)

        tweet_content = process_action_property_repository.get_property(process_action, 'tweet_content')
        tweet_content = ExpressionParser.parse(tweet_content, locals())

        tweet_hashtags = process_action_property_repository.get_property(process_action, 'tweet_hashtags')
        tweet_hashtags = ExpressionParser.parse(tweet_hashtags, locals())

        headers = json.loads(process_action_property_repository.get_property(process_action, 'headers'))
        certificate = JsonExt.loads(process_action_property_repository.get_property(process_action, 'certificate'))
        proxies = JsonExt.loads(process_action_property_repository.get_property(process_action, 'proxies'))
        url = process_action_property_repository.get_property(process_action, 'url')

        message = {
            'twitter_token': twitter_token,
            'tweet_content': tweet_content,
            'tweet_hashtags': tweet_hashtags
        }

        logger.info(job_name, json.dumps(message))
        response = RestRequest.post(headers, url, message, certificate, proxies)
        logger.info(job_name, "status_code : " + str(response.status_code) + ", reason : " + response.reason + ", content : " + response.content)

        if response.status_code != 200:
            raise ProcessException("status_code : " + str(response.status_code) + ", reason : " + response.reason + ", content : " + response.content)

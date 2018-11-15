from paprika.actions.Actionable import Actionable
from paprika.repositories.ProcessActionPropertyRepository import ProcessActionPropertyRepository
from paprika.repositories.ProcessPropertyRepository import ProcessPropertyRepository
from paprika.repositories.ProcessRepository import ProcessRepository
from paprika.system.logger.Logger import Logger
from paprika.system.JsonExt import JsonExt
from paprika.services.RestRequest import RestRequest
from paprika.actions.ProcessException import ProcessException
import json


class GetEmailSummary(Actionable):
    def __init__(self):
        Actionable.__init__(self)

    def execute(self, connector, process_action):
        logger = Logger(connector, self)
        job_name = process_action['job_name']

        process_repository = ProcessRepository(connector)
        process_property_repository = ProcessPropertyRepository(connector)
        process_action_property_repository = ProcessActionPropertyRepository(connector)

        print json.dumps(process_action)
        # retrieve the file properties
        process = process_repository.find_by_id(process_action['pcs_id'])
        print json.dumps(process)

        # retrieve the payload if present
        payload = JsonExt.loads(process_property_repository.get_property(process, 'payload'))
        mailjob_id = process_property_repository.get_property(process, 'mailjob_id')

        auth_info = json.loads(process_action_property_repository.get_property(process_action, 'auth_info'))
        headers = json.loads(process_action_property_repository.get_property(process_action, 'headers'))
        certificate = JsonExt.loads(process_action_property_repository.get_property(process_action, 'certificate'))
        proxies = JsonExt.loads(process_action_property_repository.get_property(process_action, 'proxies'))
        url = process_action_property_repository.get_property(process_action, 'url')

        message = {
            "auth_info": auth_info,
            "mailjob_id": mailjob_id
        }

        logger.info(job_name, json.dumps(message))
        response = RestRequest.post(headers, url, message, certificate, proxies)
        logger.info(job_name, "status_code : " + str(response.status_code) + ", reason : " + response.reason + ", content : " + response.content)

        if response.status_code != 200:
            message = "status_code : " + str(response.status_code) + ", reason : " + response.reason + ", content : " + response.content
            raise ProcessException(message)

        content = json.loads(response.content)
        status = content['status']
        numberOfSkipped = content['numberOfSkipped']

        if status in ['ENDED_WITH_ERRORS', 'FAILED']:
            message = "status : " + status + ", reason : " + content['error']
            raise ProcessException(message)

        if numberOfSkipped != 0:
            message = "numberOfSkipped : " + numberOfSkipped + ", reason : the email is not send but skipped. Possibly emailadress empty?"
            raise ProcessException(message)

        if not status == 'ENDED':
            return process_action


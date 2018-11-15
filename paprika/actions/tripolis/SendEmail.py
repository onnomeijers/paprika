from paprika.actions.Actionable import Actionable
from paprika.repositories.ProcessActionPropertyRepository import ProcessActionPropertyRepository
from paprika.repositories.ProcessPropertyRepository import ProcessPropertyRepository
from paprika.repositories.ProcessRepository import ProcessRepository
from paprika.system.logger.Logger import Logger
from paprika.system.JsonExt import JsonExt
from paprika.services.RestRequest import RestRequest
from paprika.actions.ProcessException import ProcessException
from paprika.system.ExpressionParser import ExpressionParser
import json


class SendEmail(Actionable):
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
        print json.dumps(payload)

        auth_info = json.loads(process_action_property_repository.get_property(process_action, 'auth_info'))
        database = process_action_property_repository.get_property(process_action, 'database')
        workspace = process_action_property_repository.get_property(process_action, 'workspace')
        contact_group = process_action_property_repository.get_property(process_action, 'contact_group')
        group_type = process_action_property_repository.get_property(process_action, 'group_type')
        direct_email_type = process_action_property_repository.get_property(process_action, 'direct_email_type')
        direct_email = process_action_property_repository.get_property(process_action, 'direct_email')

        # we are going to parse this, like in the Call action
        key_fields = json.loads(process_action_property_repository.get_property(process_action, 'key_fields'))
        key_fields = ExpressionParser.parse(key_fields, locals())
        attribute_fields = json.loads(process_action_property_repository.get_property(process_action, 'attribute_fields'))
        attribute_fields = ExpressionParser.parse(attribute_fields, locals())

        headers = json.loads(process_action_property_repository.get_property(process_action, 'headers'))
        certificate = JsonExt.loads(process_action_property_repository.get_property(process_action, 'certificate'))
        proxies = JsonExt.loads(process_action_property_repository.get_property(process_action, 'proxies'))
        url = process_action_property_repository.get_property(process_action, 'url')

        message = {
            "auth_info": auth_info,
            "database": database,
            "workspace": workspace,
            "contact_group": contact_group,
            "group_type": group_type,
            "direct_email_type": direct_email_type,
            "direct_email": direct_email,
            "key_fields": key_fields,
            "attribute_fields": attribute_fields
        }

        logger.info(job_name, json.dumps(message))
        response = RestRequest.post(headers, url, message, certificate, proxies)
        logger.info(job_name, "status_code : " + str(response.status_code) + ", reason : " + response.reason + ", content : " + response.content)

        if response.status_code != 200:
            raise ProcessException("status_code : " + str(response.status_code) + ", reason : " + response.reason + ", content : " + response.content)

        # store the returned mailjob_id in the process.
        content = json.loads(response.content)
        mailjob_id = content['mailjob_id']
        process_property_repository.set_property(process, 'mailjob_id', mailjob_id)

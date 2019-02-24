import time

from paprika.actions.Actionable import Actionable
from paprika_connector.connectors.DatasourceBuilder import DatasourceBuilder
from paprika.repositories.Clang.ClangMailSummaryRepository import ClangMailSummaryRepository
from paprika.repositories.ProcessActionPropertyRepository import ProcessActionPropertyRepository
from paprika.system.MathHelper import MathHelper
from paprika.system.Strings import Strings
from paprika.system.logger.Logger import Logger

from paprika.scrapers.Clang.Clang import Clang


class MailSummaries(Actionable):
    def __init__(self):
        Actionable.__init__(self)

    def execute(self, connector, process_action):

        job_name = process_action['job_name']

        logger = Logger(connector, self)

        process_action_property_repository = ProcessActionPropertyRepository(connector)

        # retrieve the properties
        uuid = process_action_property_repository.get_property(process_action, 'uuid')
        page_size = process_action_property_repository.get_property(process_action, 'page_size')
        datasource = process_action_property_repository.get_property(process_action, 'datasource')

        # create the scraper
        scraper = Clang()

        response = scraper.mailing_get_quickmails(uuid)
        resource_id = response.msg

        # get resource id
        resource_status = 'BUSY'
        while resource_status != "READY":
            response = scraper.resource_get_by_id(uuid, resource_id)
            resource_status = response.msg.status
            time.sleep(1)

        # get mailings
        resource_size = response.msg.size

        mailing_ids = []
        for i in xrange(0, resource_size):
            response = scraper.mailing_set_get_mailing_ids(uuid, resource_id, i, 2)
            mailing_ids.append(response.msg.integer[0])

        scraper.resource_free(uuid, resource_id)

        # get summaries
        mail_summaries = []
        for mailing_id in mailing_ids:
            response = scraper.mailing_get_by_id(uuid, mailing_id)

            campaign_name = response.msg.campaignName
            content_name = response.msg.contentName
            started_at = response.msg.startedAt
            ended_at = response.msg.endedAt
            description = response.msg.description
            received = response.msg.received
            unique_clicks = response.msg.uniqueClicks
            unique_opens = response.msg.uniqueOpens
            bounces = response.msg.bounces

            message = dict()
            message['mailing_id'] = mailing_id
            message['campaign_name'] = Strings.encode(campaign_name, 'utf-8')
            message['started_at'] = Strings.encode(started_at, 'utf-8')
            message['ended_at'] = Strings.encode(ended_at, 'utf-8')
            message['content_name'] = Strings.encode(content_name, 'utf-8')
            message['description'] = Strings.encode(description, 'utf-8')
            message['received'] = received
            message['unique_clicks'] = unique_clicks
            message['unique_opens'] = unique_opens
            message['bounces'] = bounces
            message['cor'] = MathHelper.divide(unique_opens, received) * 100.0
            message['cto'] = MathHelper.divide(unique_clicks, unique_opens) * 100.0
            message['ctr'] = MathHelper.divide(unique_clicks, received) * 100.0

            mail_summaries.append(message)

        # delete all the mailings and insert the new ones.
        mi_ds = DatasourceBuilder.find(datasource)
        clang_mail_summary_repository = ClangMailSummaryRepository(mi_ds)
        clang_mail_summary_repository.clean()
        for summary in mail_summaries:
            clang_mail_summary_repository.insert(summary)

        logger.info(job_name, 'job_name: ' + job_name)





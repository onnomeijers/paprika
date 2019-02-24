import time
from datetime import datetime
from datetime import timedelta
from paprika_connector.connectors.DatasourceBuilder import DatasourceBuilder
from paprika.executors.ManagedWorker import ManagedWorker
from paprika.processing.ProcessService import ProcessService
from paprika.repositories.EventRepository import EventRepository
from paprika.repositories.JobRepository import JobRepository
from paprika.repositories.ProcessPropertyRepository import ProcessPropertyRepository
from paprika.repositories.ScheduledEventRepository import ScheduledEventRepository
from paprika.system.logger.Logger import Logger
from paprika.system.Traceback import Traceback
from paprika_connector.connectors.ConnectorFactory import ConnectorFactory


class EventWorker(ManagedWorker):
    def __init__(self, id, settings, claim, abort, stop):
        ManagedWorker.__init__(self, id, settings, claim, abort, stop)

    def run(self, scheduled_event, test_mode=False):
        abort = self.get_abort()
        stop = self.get_stop()
        paprika_ds = DatasourceBuilder.build('paprika-ds.json')
        connector = ConnectorFactory.create_connector(paprika_ds)
        logger = Logger(connector, self)

        job_repository = JobRepository(connector)
        job = job_repository.job()
        job_name = job['job_name']

        settings = self.get_settings()
        while self.is_running():
            try:
                now = datetime.now()
                scheduled_event_repository = ScheduledEventRepository(connector)
                scheduled_event = scheduled_event_repository.find_by_hashcode(scheduled_event['hashcode'])
                job_repository = JobRepository(connector)
                event_repository = EventRepository(connector)

                repetition = scheduled_event['repetition']
                intermission = int(scheduled_event['intermission'])
                expected = datetime.strptime(scheduled_event['expected'], "%Y-%m-%d %H:%M:%S")
                next_expected = None
                if expected < now:
                    if repetition == 'HOURS':
                        next_expected = expected + timedelta(hours=int(intermission))
                        while next_expected < now:
                            next_expected += timedelta(hours=int(intermission))
                    if repetition == 'DAYS':
                        next_expected = expected + timedelta(days=int(intermission))
                        while next_expected < now:
                            next_expected += timedelta(days=int(intermission))
                    if repetition == 'MINUTES':
                        next_expected = expected + timedelta(minutes=int(intermission)) 
                        while next_expected < now:
                            next_expected += timedelta(minutes=int(intermission))

                    if next_expected:
                        message = dict()
                        message['id'] = scheduled_event['id']
                        message['expected'] = next_expected.__str__()
                        scheduled_event_repository.expected(message)

                    job = job_repository.job()
                    event_job_name = job['job_name']

                    process = ProcessService.create_process(connector, scheduled_event['pdn_id'], event_job_name, scheduled_event['e_pdn_id'])

                    event = dict()
                    event['state'] = 'READY'
                    event['repetition'] = repetition
                    event['intermission'] = intermission
                    event['expected'] = scheduled_event['expected']
                    event['job_name'] = event_job_name
                    event['pcs_id'] = process['id']
                    event = event_repository.insert(event)

                    process_property_repository = ProcessPropertyRepository(connector)
                    process_property_repository.set_property(process, 'event_id', event['id'])

                    ProcessService.execute_process(connector, process)

                # check if we need to abort, can be called from the main thread or other thread
                aborted = abort.is_aborted()
                self.running(not aborted)

                # check if we need to stop, will be set by the agent's WatchWorker thread
                if not aborted:
                    stopped = stop.is_stopped()
                    self.running(not stopped)

                # check for test_mode, break the loop
                if test_mode:
                    self.running(False)

                connector.close()
                time.sleep(settings['worker_idle_delay'])
                logger.trace(job_name, 'worker #' + str(self.get_id()) + " executed.")
            except:
                aborted = abort.is_aborted()
                self.running(not aborted)

                if not aborted:
                    stopped = stop.is_stopped()
                    self.running(not stopped)

                result = Traceback.build()
                logger.fatal(job_name, result['message'], result['backtrace'])
                connector.close()
                time.sleep(settings['worker_exception_delay'])

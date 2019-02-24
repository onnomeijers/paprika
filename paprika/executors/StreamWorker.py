import time
from paprika_connector.connectors.DatasourceBuilder import DatasourceBuilder
from paprika.executors.MessageWorker import ManagedWorker
from paprika.repositories.JobRepository import JobRepository
from paprika.scrapers.StreamScraper import StreamScraper
from paprika.system.logger.Logger import Logger
from paprika.system.Traceback import Traceback
from paprika_connector.connectors.ConnectorFactory import ConnectorFactory


class StreamWorker(ManagedWorker):
    def __init__(self, id, settings, claim, abort, stop):
        ManagedWorker.__init__(self, id, settings, claim, abort, stop)

    def run(self, stream):
        job_name = ''
        abort = self.get_abort()
        stop = self.get_stop()
        settings = self.get_settings()

        paprika_ds = DatasourceBuilder.build('paprika-ds.json')
        connector = ConnectorFactory.create_connector(paprika_ds)
        logger = Logger(connector, self)

        job_repository = JobRepository(connector)
        job = job_repository.job()
        job_name = job['job_name']
        logger.trace(job_name, 'worker #' + str(self.get_id()) + " started.")

        while self.is_running():
            try:
                url = stream['url']
                username = stream['username']
                password = stream['password']
                auth = (username, password)

                # when streaming works the code stops here.
                # this is the reason why we use a Process instead of a Thread. A process can be terminated.
                StreamScraper.listen(connector, job_name, stream, url, auth)

                # check if we need to abort, can be called from the main thread or other thread
                aborted = abort.is_aborted()
                self.running(not aborted)

                # check if we need to stop, will be set by the agent's WatchWorker thread
                if not aborted:
                    stopped = stop.is_stopped()
                    self.running(not stopped)
                connector.close()
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

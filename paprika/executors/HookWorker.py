import json
import time
from paprika_connector.connectors.DatasourceBuilder import DatasourceBuilder
from paprika.executors.ManagedWorker import ManagedWorker
from paprika.processing.ProcessService import ProcessService
from paprika.repositories.ChunkRepository import ChunkRepository
from paprika.repositories.JobRepository import JobRepository
from paprika.repositories.PayloadRepository import PayloadRepository
from paprika.repositories.ProcessPropertyRepository import ProcessPropertyRepository
from paprika.repositories.RuleRepository import RuleRepository
from paprika.system.logger.Logger import Logger
from paprika.system.match.DictionaryMethod import DictionaryMethod
from paprika.system.match.Matcher import Matcher
from paprika.system.Traceback import Traceback
from paprika_connector.connectors.ConnectorFactory import ConnectorFactory
from paprika.repositories.DatasourceRepository import DatasourceRepository


class HookWorker(ManagedWorker):
    def __init__(self, id, settings, claim, abort, stop):
        ManagedWorker.__init__(self, id, settings, claim, abort, stop)

    def run(self, hook):
        abort = self.get_abort()
        claim = self.get_claim()
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

                rule_repository = RuleRepository(connector)
                chunk_repository = ChunkRepository(connector)

                # retrieve the next payload
                datasource = hook['datasource']
                datasource_repository = DatasourceRepository(connector)
                payload_ds = datasource_repository.get_by_name(datasource)
                payload_c = ConnectorFactory.create_connector(payload_ds)
                payload_repository = PayloadRepository(payload_c)
                payload = payload_repository.dequeue(claim, hook)
                payload_c.close()

                if payload:
                    # ask for a new job_name
                    job = job_repository.job()
                    payload_job_name = job['job_name']

                    # find the rule
                    found_rule = None
                    rules = rule_repository.find_by_hook(hook)
                    for rule in rules:
                        if Matcher.match(DictionaryMethod, rule['pattern'], payload):
                            found_rule = rule

                    # store the payload as chunk in paprika
                    process = ProcessService.create_process(connector, found_rule['pdn_id'], payload_job_name, found_rule['e_pdn_id'])

                    chunk = dict()
                    chunk['job_name'] = payload_job_name
                    chunk['pcs_id'] = process['id']
                    chunk['state'] = 'READY'
                    chunk['datasource'] = datasource
                    chunk['tablename'] = hook['tablename']
                    chunk['selector'] = hook['selector']
                    chunk['updater'] = hook['updater']
                    chunk['options'] = hook['options']
                    chunk['payload'] = json.dumps(payload)
                    chunk['rle_id'] = found_rule['id']
                    chunk['rule'] = found_rule['rule']
                    chunk['pattern'] = found_rule['pattern']
                    chunk = chunk_repository.insert(chunk)

                    process_property_repository = ProcessPropertyRepository(connector)
                    process_property_repository.set_property(process, 'chunk_id', chunk['id'])
                    process_property_repository.set_property(process, 'payload', chunk['payload'])

                    ProcessService.execute_process(connector, process)

                # check if we need to abort, can be called from the main thread or other thread
                aborted = abort.is_aborted()
                self.running(not aborted)

                # check if we need to stop, will be set by the agent's WatchWorker thread
                if not aborted:
                    stopped = stop.is_stopped()
                    self.running(not stopped)

                # no payload to process
                if not payload:
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
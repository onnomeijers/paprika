import time
import json
from paprika_connector.connectors.DatasourceBuilder import DatasourceBuilder
from paprika.executors.ManagedWorker import ManagedWorker
from paprika.processing.ProcessService import ProcessService
from paprika.repositories.FileRepository import FileRepository
from paprika.repositories.JobRepository import JobRepository
from paprika.repositories.ProcessPropertyRepository import ProcessPropertyRepository
from paprika.repositories.PropertyRepository import PropertyRepository
from paprika.repositories.RuleRepository import RuleRepository
from paprika.system.logger.Logger import Logger
from paprika.system.match.Matcher import Matcher
from paprika.system.match.ReMethod import ReMethod
from paprika.vfs.VfsFactory import VfsFactory
from paprika.system.Traceback import Traceback
from paprika_connector.connectors.ConnectorFactory import ConnectorFactory


class FileWorker(ManagedWorker):
    def __init__(self, id, settings, claim, abort, stop):
        ManagedWorker.__init__(self, id, settings, claim, abort, stop)

    def run(self, location):
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
                properties = PropertyRepository(connector)
                registry = FileRepository(connector)
                rule_repository = RuleRepository(connector)

                excluded_extensions = properties.get_property('scanner.excluded_extensions')
                stable_check_delay = properties.get_property('scanner.stable_check_delay')

                url = location['url']
                patterns = location['patterns']
                client = VfsFactory.create_client(url)
                client.set_excluded_extensions(excluded_extensions)
                client.set_stable_check_delay(int(stable_check_delay))
                client.set_regular_expressions(patterns)
                path = client.get_path()
                recursive = int(location['recursive'])
                depth = int(location['depth'])

                client.connect()
                files = client.list_stable(path, recursive=recursive, depth=depth)
                for file in files:
                    registered_file = registry.get_by_hashcode(file['hashcode'])
                    if not registered_file:

                        # find the rule
                        found_rule = None
                        rules = rule_repository.find_by_location(location)
                        for rule in rules:
                            if Matcher.match(ReMethod, rule['pattern'], file['filename']):
                                found_rule = rule
                        if not found_rule:
                            found_rule = rule_repository.find_failsafe()

                        job = job_repository.job()
                        file_job_name = job['job_name']

                        logger.info(file_job_name,
                                    "file: " + file['url'] + '/' + file['filename'] + " rule: " + found_rule[
                                        'rule'] + " hascode:" + file['hashcode'])

                        process = ProcessService.create_process(connector, found_rule['pdn_id'], file_job_name, found_rule['e_pdn_id'])

                        message = dict()
                        message['job_name'] = file_job_name
                        message['filename'] = file['filename']
                        message['path'] = file['path']
                        message['pattern'] = found_rule['pattern']
                        message['rle_id'] = found_rule['id']
                        message['rule'] = found_rule['rule']
                        message['pickup_location'] = file['url']
                        message['filesize'] = file['size']
                        message['hashcode'] = file['hashcode']
                        message['pcs_id'] = process['id']
                        message['state'] = 'READY'
                        registered_file = registry.insert(message)

                        process_property_repository = ProcessPropertyRepository(connector)
                        process_property_repository.set_property(process, 'file_id', registered_file['id'])
                        process_property_repository.set_property(process, 'pickup_location', file['url'])
                        process_property_repository.set_property(process, 'path', file['path'])
                        process_property_repository.set_property(process, 'payload', json.dumps({'filename': file['filename'], 'job_name': file_job_name}))

                        ProcessService.execute_process(connector, process)

                client.close()

                # check if we need to abort, can be called from the main thread or other thread
                aborted = abort.is_aborted()
                self.running(not aborted)

                # check if we need to stop, will be set by the agent's WatchWorker thread
                if not aborted:
                    stopped = stop.is_stopped()
                    self.running(not stopped)

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

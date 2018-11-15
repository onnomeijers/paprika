import json
from paprika.consumers.Consumable import Consumable
from paprika.processing.ProcessService import ProcessService
from paprika.repositories.JobRepository import JobRepository
from paprika.repositories.ProcessPropertyRepository import ProcessPropertyRepository
from paprika.repositories.RuleRepository import RuleRepository
from paprika.repositories.StreamRepository import StreamRepository
from paprika.system.match.DictionaryMethod import DictionaryMethod
from paprika.system.match.Matcher import Matcher
from paprika.repositories.ChunkRepository import ChunkRepository


class StreamProcessor(Consumable):
    def __init__(self):
        Consumable.__init__(self)

    def action(self, connector, message):
        stream_repository = StreamRepository(connector)
        payload = json.loads(message['payload'])
        stream = stream_repository.find_by_hashcode(payload['oxyma.stream.hashcode'])

        rule_repository = RuleRepository(connector)
        chunk_repository = ChunkRepository(connector)

        # ask for a new job_name
        job_repository = JobRepository(connector)
        job = job_repository.job()
        job_name = job['job_name']

        # find the rule
        found_rule = None
        rules = rule_repository.find_by_stream(stream)
        for rule in rules:
            if Matcher.match(DictionaryMethod, json.loads(rule['pattern']), payload):
                found_rule = rule

        # only start a process when a rule is found,
        # if the rule is not found, the given payload is simply ignored
        if found_rule:

            # store the payload as chunk in paprika
            process = ProcessService.create_process(connector, found_rule['pdn_id'], job['job_name'], found_rule['e_pdn_id'])

            chunk = dict()
            chunk['job_name'] = job_name
            chunk['pcs_id'] = process['id']
            chunk['state'] = 'READY'
            chunk['datasource'] = ''
            chunk['tablename'] = ''
            chunk['selector'] = ''
            chunk['options'] = ''
            chunk['payload'] = json.dumps(payload)
            chunk['rle_id'] = found_rule['id']
            chunk['rule'] = found_rule['rule']
            chunk['pattern'] = found_rule['pattern']
            chunk['updater'] = ''
            chunk = chunk_repository.insert(chunk)

            process_property_repository = ProcessPropertyRepository(connector)
            process_property_repository.set_property(process, 'chunk_id', chunk['id'])

            ProcessService.execute_process(connector, process)

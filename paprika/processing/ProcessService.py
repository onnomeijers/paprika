from paprika.messaging.Message import Message
from paprika.repositories.ProcessRepository import ProcessRepository
from paprika.repositories.ProcessDefinitionRepository import ProcessDefinitionRepository


class ProcessService:
    def __init__(self):
        pass

    @staticmethod
    def create_process(connector, pdn_id, job_name, e_pdn_id=None):
        process_definition_repository = ProcessDefinitionRepository(connector)
        process_definition = process_definition_repository.find_by_id(pdn_id)

        # create a process instance, based on the given process definition
        process_repository = ProcessRepository(connector)

        process = dict()
        process["job_name"] = job_name
        process["pdn_id"] = process_definition["id"]
        process["e_pdn_id"] = e_pdn_id
        process["state"] = 'READY'
        process["name"] = process_definition["name"]
        process["queue"] = process_definition["queue"]
        process = process_repository.insert(process)

        return process

    @staticmethod
    def execute_process(connector, process):
        payload = process
        Message.enqueue(connector, process['queue'], payload, 'message', 'paprika.consumers.ProcessStart.ProcessStart')

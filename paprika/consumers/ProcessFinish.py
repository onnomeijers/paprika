import json
from paprika.consumers.Consumable import Consumable
from paprika.repositories.ProcessRepository import ProcessRepository
from paprika.system.Traceback import Traceback
from paprika.system.logger.Logger import Logger


class ProcessFinish(Consumable):
    def __init__(self):
        Consumable.__init__(self)

    def action(self, connector, message):
        try:
            process = json.loads(message['payload'])
            process_repository = ProcessRepository(connector)

            process['state'] = 'PROCESSED'
            process['message'] = ''
            process['backtrace'] = ''
            process_repository.state(process)
        except:
            process = json.loads(message['payload'])
            process_repository = ProcessRepository(connector)
            result = Traceback.build()
            result['id'] = process['id']
            result['state'] = 'FAILED'
            process_repository.state(result)

            logger = Logger(connector, self)
            logger.fatal(process['job_name'], result['message'], result['backtrace'])

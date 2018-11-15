from paprika.repositories.MessageRepository import MessageRepository
from paprika.repositories.QueueRepository import QueueRepository
import json


class Message:
    def __init__(self):
        pass

    @staticmethod
    def enqueue(connector, queue_name, payload, agent,  consumer):
        queue_repository = QueueRepository(connector)
        queue = queue_repository.find_by_name(queue_name)

        message_repository = MessageRepository(connector)

        message = dict()
        message['state'] = 'READY'
        message['delay'] = None
        message['payload'] = json.dumps(payload)
        message['agent'] = agent
        message['consumer'] = consumer
        result = message_repository.insert(queue, message)

        return result

    @staticmethod
    def enqueue_wait(connector, queue_name, delay, payload, agent, consumer):
        queue_repository = QueueRepository(connector)
        queue = queue_repository.find_by_name(queue_name)

        message_repository = MessageRepository(connector)

        message = dict()
        message['state'] = 'WAIT'
        message['delay'] = delay
        message['payload'] = json.dumps(payload)
        message['agent'] = agent
        message['consumer'] = consumer
        result = message_repository.insert(queue, message)

        return result

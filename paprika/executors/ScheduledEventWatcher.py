from paprika.executors.EventWorker import EventWorker
from paprika.repositories.ScheduledEventRepository import ScheduledEventRepository
from paprika.threads.Runner import Runner
from paprika.threads.Stop import Stop
from paprika.threads.Claim import Claim


class ScheduledEventWatcher(object):
    def __init__(self):
        object.__init__(self)

    def watch(self, connector, settings, threads, abort):
        scheduled_event_repository = ScheduledEventRepository(connector)
        schedules = scheduled_event_repository.list()
        for schedule in schedules:
            if not threads.has_group(schedule['hashcode']) and schedule['active'] == '1':
                stop = Stop()
                claim = Claim()
                id = threads.next_id()
                t = Runner.run(EventWorker(id, settings, claim, abort, stop), schedule)
                threads.append({'id': id, 'group': schedule['hashcode'], 'thread': t, 'stop': stop})
            if threads.has_group(schedule['hashcode']) and schedule['active'] == '0':
                stop = threads.list_by_group(schedule['hashcode'])[0]['stop']
                stop.stopped(True)
                threads.remove_by_group(schedule['hashcode'])

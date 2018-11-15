from paprika.executors.FileWorker import FileWorker
from paprika.repositories.LocationRepository import LocationRepository
from paprika.threads.Runner import Runner
from paprika.threads.Stop import Stop
from paprika.threads.Claim import Claim


class LocationWatcher(object):
    def __init__(self):
        object.__init__(self)

    def watch(self, connector, settings, threads, abort):
        location_repository = LocationRepository(connector)
        locations = location_repository.list()
        for location in locations:
            if not threads.has_group(location['hashcode']) and location['active'] == '1':
                stop = Stop()
                claim = Claim()
                id = threads.next_id()
                t = Runner.run(FileWorker(id, settings, claim, abort, stop), location)
                threads.append({'id': id, 'group': location['hashcode'], 'thread': t, 'stop': stop})
            if threads.has_group(location['hashcode']) and location['active'] == '0':
                stop = threads.list_by_group(location['hashcode'])[0]['stop']
                stop.stopped(True)
                threads.remove_by_group(location['hashcode'])

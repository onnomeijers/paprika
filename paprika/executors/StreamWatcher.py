import time
from paprika.executors.StreamWorker import StreamWorker
from paprika.repositories.StreamRepository import StreamRepository
from paprika.multi.Launcher import Launcher
from paprika.multi.Stop import Stop
from paprika.multi.Claim import Claim


class StreamWatcher(object):
    def __init__(self):
        object.__init__(self)

    def watch(self, connector, settings, threads, abort):
        stream_repository = StreamRepository(connector)
        streams = stream_repository.list()
        for stream in streams:
            if not threads.has_group(stream['hashcode']) and stream['active'] == '1':
                stop = Stop()
                claim = Claim()
                id = threads.next_id()
                t = Launcher.run(StreamWorker(id, settings, claim, abort, stop), stream)
                threads.append({'id': id, 'group': stream['hashcode'], 'thread': t, 'stop': stop})
            if threads.has_group(stream['hashcode']) and stream['active'] == '0':
                # try to stop the stream. This will probably not work. It is locked in the stream
                stop = threads.list_by_group(stream['hashcode'])[0]['stop']
                stop.stopped(True)

                # wait one second, after that terminate the stream, if it is alive.
                time.sleep(1)
                threads.terminate_by_group(stream['hashcode'])
                threads.remove_by_group(stream['hashcode'])

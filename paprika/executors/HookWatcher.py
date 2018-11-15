from paprika.executors.HookWorker import HookWorker
from paprika.repositories.HookRepository import HookRepository
from paprika.threads.Runner import Runner
from paprika.threads.Stop import Stop
from paprika.threads.Claim import Claim


class HookWatcher(object):
    def __init__(self):
        object.__init__(self)

    def watch(self, connector, settings, threads, abort):
        hook_repository = HookRepository(connector)
        hooks = hook_repository.list()
        for hook in hooks:
            if not threads.has_group(hook['hashcode']) and hook['active'] == '1':
                stop = Stop()
                claim = Claim()
                pool_size = settings['pool_size']
                for i in range(0, pool_size):
                    id = threads.next_id()
                    t = Runner.run(HookWorker(id, settings, claim, abort, stop), hook)
                    threads.append({'id': id, 'group': hook['hashcode'], 'thread': t, 'stop': stop})
            if threads.has_group(hook['hashcode']) and hook['active'] == '0':
                stop = threads.list_by_group(hook['hashcode'])[0]['stop']
                stop.stopped(True)
                threads.remove_by_group(hook['hashcode'])

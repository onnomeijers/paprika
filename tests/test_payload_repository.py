import unittest
from paprika_connector.connectors.DatasourceBuilder import DatasourceBuilder
from paprika_connector.connectors.ConnectorFactory import ConnectorFactory
from paprika.repositories.PayloadRepository import PayloadRepository
from paprika.repositories.HookRepository import HookRepository
from paprika.threads.Claim import Claim


class TestPayloadRepository(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_payload(self):
        # retrieve the next payload

        paprika_ds = DatasourceBuilder.build('paprika-ds.json')
        connector = ConnectorFactory.create_connector(paprika_ds)

        hook_repository = HookRepository(connector)
        hooks = hook_repository.list_active()

        # retrieve the first hook, not the best method but for now it works
        # expected to retrieve the hook to send an offer (nuon).
        hook = hooks[0]
        print hook

        claim = Claim()

        payload_ds = DatasourceBuilder.find(connector, hook['datasource'])
        payload_c = ConnectorFactory.create_connector(payload_ds)
        payload_repository = PayloadRepository(payload_c)
        #payload = payload_repository.dequeue(claim, hook)
        payload = payload_repository.next(hook)
        print payload
        print payload['proces_bestelling_id']

        payload_repository.state(hook, payload, 'READY')

        # options = json.loads(hook['options'])
        #
        # state = 'READY'
        # #options = [{'status': '#state'}, {'proces_bestelling_id': '#payload.proces_bestelling_id'}]
        # options = ExpressionParser.parse(options, locals())





        # payload_repository.state(hook, payload, 'READY')
        payload_c.close()



if __name__ == '__main__':
    unittest.main()

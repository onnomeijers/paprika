import json
import unittest
from paprika.connectors.ConnectorFactory import ConnectorFactory
from paprika.connectors.DatasourceBuilder import DatasourceBuilder
from paprika.repositories.JobRepository import JobRepository
from paprika.repositories.ProcessActionPropertyRepository import ProcessActionPropertyRepository
from paprika.repositories.ProcessActionRepository import ProcessActionRepository
from paprika.repositories.ProcessPropertyRepository import ProcessPropertyRepository
from paprika.repositories.ProcessRepository import ProcessRepository
from paprika.actions.files.Copy import Copy
from paprika.repositories.EventRepository import EventRepository


class TestCall(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_call(self):
        paprika_ds = DatasourceBuilder.build('paprika-ds.json')
        connector = ConnectorFactory.create_connector(paprika_ds)

        job_repository = JobRepository(connector)
        job_name = job_repository.job()

        process_respository = ProcessRepository(connector)
        process = dict()
        process['job_name'] = job_name['job_name']
        process['pdn_id'] = None
        process['state'] = None
        process['e_pdn_id'] = None
        process['name'] = None
        process['queue'] = None
        process_respository.insert(process)

        event_respository = EventRepository(connector)
        event = dict()
        event['job_name'] = job_name['job_name']
        event['state'] = None
        event['repetition'] = 'DAYS'
        event['intermission'] = '1'
        event['pcs_id'] = process['id']
        event_respository.insert(event)

        process_property_repository = ProcessPropertyRepository(connector)
        process_property_repository.set_property(process, 'event_id', event['id'])

        process_action_repository = ProcessActionRepository(connector)
        process_action = dict()
        process_action['job_name'] = job_name['job_name']
        process_action['pcs_id'] = process['id']
        process_action['dan_id'] = None
        process_action['name'] = 'copy'
        process_action['state'] = 'processed'
        process_action_repository.insert(process_action)

        process_action_property_repository = ProcessActionPropertyRepository(connector)
        process_action_property = dict()
        process_action_property['name'] = 'file_id'
        process_action_property['value'] = 1
        process_action_property['pan_id'] = process_action['id']
        process_action_property_repository.insert(process_action_property)

        copy = Copy()
        copy.execute(connector, process_action)

        connector.close()


if __name__ == '__main__':
    unittest.main()

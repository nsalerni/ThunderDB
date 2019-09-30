import unittest
from single_node_server import local_mode
from threading import Thread
import time
import json
import thunderdb.compute.utils as request


SAMPLE_DATA_FILE = "sample_data/data_demo_small.txt"
NODE_IP_ADDRESS = "localhost"


class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.process = Thread(target=local_mode, kwargs=dict(data_file=SAMPLE_DATA_FILE))
        cls.process.daemon = True
        cls.process.start()

        # Wait for the HTTP server to start and load the initial dataset
        time.sleep(5)

    def test_get_existing_key(self):
        key = "foo"
        expected_value = "bar"
        response = request.get('http://' + NODE_IP_ADDRESS + '/get/{}'.format(key))

        self.assertEqual(len(response.json().keys()), 1)
        self.assertEqual(response.json()[key], expected_value)

    def test_get_non_existent_key(self):
        key = "foo1"
        response = request.get('http://' + NODE_IP_ADDRESS + '/get/{}'.format(key))
        self.assertEqual(response.status_code, 404)

    def test_put_new_key(self):
        key = "new_foo"
        value = "new_bar"
        payload = {key: value}
        request.post('http://' + NODE_IP_ADDRESS + '/put', data=json.dumps(payload))

        # Ensure the new key-value pair exists in the store
        response = request.get('http://' + NODE_IP_ADDRESS + '/get/{}'.format(key))
        self.assertEqual(response.json()[key], value)

    @classmethod
    def tearDownClass(cls):
        cls.process.join(timeout=1)


if __name__ == '__main__':
    unittest.main()

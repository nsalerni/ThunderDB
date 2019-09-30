import thunderdb.compute.utils as request
import json


class Node(object):
    """Object representing a node in the cluster

    This class provides functions to get and set key-value pairs, 
    set the replica for the key-value pair, and update the node's 
    configuration
    """
    @staticmethod
    def put(node_ip_address, key, value):
        """Set a key-value pair on a specific node
        """
        payload = {key: value}
        request.post('http://' + node_ip_address + '/put', data=json.dumps(payload))

    @staticmethod
    def get(node_ip_address, key):
        """Get the value for a given key from a specific node
        """
        response = request.get('http://' + node_ip_address + '/get/{}'.format(key))
        return response.json()

    @staticmethod
    def put_in_replica(node_ip_address, key, value):
        """Replicate a key-value pair on another node (uses Consistent Hasing) 
        """
        payload = {key: value}
        request.post('http://' + node_ip_address + '/replicate', data=json.dumps(payload))
    
    @staticmethod
    def update_configuration_for_node(node_ip_address, configuration):
        request.post('http://' + node_ip_address + '/update-node-configuration', data=json.dumps(configuration))

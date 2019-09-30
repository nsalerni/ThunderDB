import concurrent.futures
import copy

from thunderdb.storage.in_memory_store import InMemoryStore
from thunderdb.hashing.consistent_hashing import ConsistentHash
from thunderdb.compute.node import Node


class Engine(object):
    """A class responsible for all the operations that can be performed in the app
    """
    def __init__(self, config):
        self.config = config
        self.storage = InMemoryStore()

    def put(self, key, value):
        """Put a key-pair into the right node(s) in the cluster

        We will use Consistent Hashing to find the correct id of the node where
        the key-value pair should be stored. We also create a replica for the
        key-value pair on an adjacent node
        """
        if len(self.config.nodes.keys()) == 1:
            self.storage.put(key, value)
        else:
            node_id = ConsistentHash(len(self.config.nodes)).get_node_id(key)
            if node_id == self.config.node_id:
                # Store the value in the current node!
                self.storage.put(key, value)
            else:
                Node.put(self.config.nodes[node_id], key, value)

    def batch_put(self, data_file):
        """Insert all entries from a file into the key-value store

        The intended use of this function is to load data at initialization,
        however, this can be adapted to batching data through HTTP calls
        """
        import time
        start_time = time.time()

        import pandas as pd
        chunksize = 10000
        for chunk in pd.read_csv(data_file, sep=" ", chunksize=chunksize, names=["key", "value"]):
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                [executor.submit(self.put, row["key"], row["value"]) for _, row in chunk.iterrows()]

        print("Finished loading initial dataset... Took {} seconds...".format(time.time() - start_time))

    def replicate(self, key, value):
        self.storage.put(key, value)

    def get(self, key):
        """Get the value associated with a given key

        This function will find the node that contains the
        corresponding data by using Consistent Hashing
        """
        # Try to lookup the key in the current node.
        # In some cases, we may get a hit without the overhead
        # of searching for the key in another node in the cluster.
        value = self.storage.get(key)
        if value is not None:
            return value

        # In the case where the value is not in the current node,
        # determine which node to perform the lookup in by using Consistent Hashing
        node_id = ConsistentHash(len(self.config.nodes)).get_node_id(key)
        if node_id == self.config.node_id:
            # We've already tried searching in our current node, therefore,
            # the key does not exist in our key-value store
            return None
        return Node.get(self.config.nodes[node_id], key)[key]

    def update_cluster_configuration_with_node_config(self):
        """Update all nodes in the cluster with the current node's configuration
        """
        nodes = copy.deepcopy(self.config.nodes)
        for node_id, node_ip in nodes.items():
            if node_id != self.config.node_id:
                Node.update_configuration_for_node(node_ip, nodes)

    def update_cluster_configuration_and_redistribute(self, configuration):
        """Update the configuration of the cluster

        This function will redistribute the data after the configuration
        has been modified. For example, if we add a new node, it may inherit
        some data from its adjacent node in the cluster.
        """
        updated_configuration = self.config.add(configuration)
        if updated_configuration:
            self.redistribute()
            self.update_cluster_configuration_with_node_config()

    def redistribute(self):
        """Redistribute the key-value pairs accross all nodes according to the latest config
        """
        kv_store = copy.deepcopy(self.storage.data)
        for key, value in kv_store.items():
            self.put(key, value)

            node_id = ConsistentHash(len(self.config.nodes)).get_node_id(key)
            if (node_id != self.config.node_id and
               (node_id + 1) % len(self.config.nodes) != self.config.node_id):
                # Remove the key-value pair from the node it no longer belongs in
                self.storage.delete(key)

    def snapshot(self):
        """Return a snapshot of the data in the current node
        """
        return self.storage.data

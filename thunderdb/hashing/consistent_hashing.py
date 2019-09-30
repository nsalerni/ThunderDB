import bisect
import hashlib


class ConsistentHash:
    """Create a consistent hash for a cluster of size n

    The class gives you the ability to specify how many replicas
    to create for your data, giving us redundancy in our application.

    ConsistentHash has a total of three atrributes:

        - num_nodes: the number of nodes in your cluster
        - num_replicas: the number of replicas to create
        - consistent_hash_tuples: a list of tuples that (n, m, k), where:
            - n ranges over the number of nodes
            - m ranges over the number of replicas
            - j ranges over the possible hash values (creating the ring)
    """
    def __init__(self, num_nodes=1):
        self.num_nodes = num_nodes
        hash_tuples = [(n, self._hash(str(n))) for n in range(self.num_nodes)]
        hash_tuples.sort(key=lambda x: x[1])  # sort based on hash values
        self.hash_tuples = hash_tuples

    def get_node_id(self, key):
        """Get the node id of the node which the key gets sent to
        """
        hash_value = self._hash(key)
        
        # Edge Case: Cycle past hash value of 1 and we loop back around to 0.
        if hash_value > self.hash_tuples[-1][1]:
            return self.hash_tuples[0][0]

        hash_values = list(map(lambda x: x[1], self.hash_tuples))
        index = bisect.bisect_left(hash_values, hash_value)
        return self.hash_tuples[index][0]

    @staticmethod
    def _hash(key):
        """Returns a hash for the key in the range of [0,1)
        """
        return (int(hashlib.md5(key.encode()).hexdigest(), 16) % 1000000) / 1000000.0

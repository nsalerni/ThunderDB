class Config(object):
    """Configuration object for the cluster
    """
    def __init__(self, node_id, node_ip, next_node_id, next_node_ip):
        self.node_id = node_id
        self.node_ip = node_ip
        self.next_node_ip = next_node_ip
        self.nodes = {
            self.node_id: self.node_ip,
            next_node_id: next_node_ip
        }

    def __repr__(self):
        return "{}".format(self.nodes)

    def add(self, conf):
        """Add new nodes to the configuration

        We return a value indicating whether or not there 
        was a change to the dictionary:
            (False -> no change, True -> change)
        """
        previous_size = len(self.nodes.keys())
        self.nodes.update(conf)
        return previous_size != len(self.nodes.keys())

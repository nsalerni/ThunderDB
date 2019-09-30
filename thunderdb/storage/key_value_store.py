from abc import abstractmethod


class KeyValueStore(object):
    """This abstract class defines the contract for concrete Key-Value store implementations
    """

    @abstractmethod
    def put(self, key, value):
        """Store a key-value pair into the store
        """
        pass

    @abstractmethod
    def get(self, key):
        """Get the value associated with a particular key
        """
        pass

    @abstractmethod
    def delete(self, key):
        """Delete the given key from the store
        """
        pass

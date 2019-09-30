from thunderdb.storage.key_value_store import KeyValueStore


class InMemoryStore(KeyValueStore):
    """An in-memory implementation of the KeyValueStore

    In this class, storage is handled by Python's built-in dictionary
    """
    def __init__(self):
        self.data = dict()

    def put(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key, None)

    def delete(self, key):
        self.data.pop(key, None)

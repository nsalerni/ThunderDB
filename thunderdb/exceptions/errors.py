class KeyValueStoreException(Exception):
    """An exception when a value is not found in the key-value store
    """
    code = 400

    def __init__(self, *args, **kwargs):
        super(KeyValueStoreException, self).__init__(*args)
        self.kwargs = kwargs


class ServiceError(KeyValueStoreException):
    """A 500-level HTTP error for the service 
    """
    code = 500

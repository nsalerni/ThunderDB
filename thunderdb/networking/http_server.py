"""
A lightweight implementation of a multi-threaded HTTP server
"""
from thunderdb.exceptions.errors import KeyValueStoreException
import json
import time
import threading

from thunderdb.compute.engine import Engine
from bottle import Bottle, request, response, abort


def initialize(config, data_file=None):
    """Initialize the application with the given configuration

    In this instance, the application uses Bottle as the HTTP Server
    framework because it is lightweight and provides a simple API. Any
    other framework, like Flask, could be used in its place depending on
    your application's needs
    """
    app = Bottle()
    engine = Engine(config)

    def update_configuration():
        """Update the configuration for the given application

        This is only used as a target for our threads
        """
        time.sleep(2)  # Wait for our other nodes to be ready
        engine.update_cluster_configuration_with_node_config()

    # Execute this function in a new thread, so the main thread remains uninterrupted
    update_configuration_thread = threading.Thread(target=update_configuration)
    update_configuration_thread.start()

    def load_data():
        """Load an initial dataset into our key-value store
        """
        time.sleep(3)  # Wait for our other nodes to be ready
        engine.batch_put(data_file)

    if data_file:
        # Load the initial dataset in a new thread, so the main thread remains uninterrupted
        load_data_thread = threading.Thread(target=load_data)
        load_data_thread.start()

    @app.error()
    @app.error(404)
    def handle_error(error):
        message = str(error.exception) if error.exception else str()
        resp = {
            'exception_type': type(error.exception).__name__
        }

        if issubclass(type(error.exception), KeyValueStoreException):
            response.status = error.exception.code
            resp.update(error.exception.extra_data)
        else:
            response.status = error.status_code

        response.set_header('Content-type', 'application/json')
        return '{} {}: {}'.format(response.status, message, error.body)

    @app.route('/ping', method=['GET'])
    def ping():
        """Ping the node to see if its active
        """
        return {
            'service': 'node',
            'status': 'OK'
        }

    @app.route('/put', method=['POST'])
    def put():
        """Put a key-value pair into the key-value store
        """
        data = json.loads(request.body.read())

        if len(data.keys()) != 1:
            abort(400, "The request data is not valid.. "
                       "Please provide exactly one key-value pair")

        key, value = next(iter(data.items()))
        engine.put(key, value)
        return

    @app.route('/replicate', method=['POST'])
    def replicate():
        """Put the key-value pair in the replica node
        """
        data = json.loads(request.body.read())

        if len(data.keys()) != 1:
            abort(400, "The request data is not valid.. "
                       "Please provide exactly one key-value pair")

        key, value = next(iter(data.items()))
        engine.replicate(key, value)
        return

    @app.route('/get/<key>', method=['GET'])
    def get(key):
        """Get the value for the given key from the key-value store
        """
        value = engine.get(key)
        if value:
            return {key: value}
        else:
            abort(404, "The key '{}' was not found in the key-value store".format(key))

    @app.route('/update-node-configuration', method=['POST'])
    def update_node_configuration():
        """Update the configuration for a node
        """
        request_body = json.loads(request.body.read())
        configuration = {}
        for node_id in request_body:
            configuration[int(node_id)] = request_body[node_id]
        engine.update_cluster_configuration_and_redistribute(configuration)

    @app.route('/snapshot', method=['GET'])
    def snapshot():
        """Dump a snapshot of the data for the current node
        """
        return engine.snapshot()

    return app

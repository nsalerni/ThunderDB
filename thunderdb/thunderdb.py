import os
from argparse import ArgumentParser

from thunderdb.networking.http_server import initialize
from thunderdb.config import Config


def get_argument_parser():
    """Configures a parser for command-line arguments

    Returns:
        ArgumentParser: Built-in parser for command-line options, arguments
    """
    parser = ArgumentParser(description='The CLI for our key-value server for immutable data')
    parser.add_argument('-d', '--data',
                        required=True,
                        help="Path to the file which contains the key-value pairs you want to load")
    return parser


def parse_arguments():
    """Parses command line arguments, returning options and a list of tasks

    Returns:
        Namespace: Simple class used by default by parse_args() to create an
                   object holding attributes and return it
    """
    parser = get_argument_parser()
    arguments = parser.parse_args()

    for error in validate_arguments(arguments):
        parser.error(error)

    return arguments


def validate_arguments(arguments):
    """Validates that all the arguments are valid

    Yields:
        Errors, if any
    """
    if not os.path.exists(arguments.data) or not os.path.isfile(arguments.data):
        yield "The data file you provided does not exist..."

    return


def main():
    """Launch the server and start listening for requests
    """
    node_id = int(os.environ.get('NODE_ID'))
    node_ip = os.environ.get('NODE_IP')
    next_node_id = int(os.environ.get('NEXT_NODE_ID'))
    next_node_ip = os.environ.get('NEXT_NODE_IP')

    relative_path_to_data_file = os.environ.get('DATA_FILE')

    config = Config(node_id, node_ip, next_node_id, next_node_ip)
    app = initialize(config, relative_path_to_data_file)
    app.run(host='0.0.0.0', port=80, server='waitress', threads=6, loglevel='warning')


if __name__ == "__main__":
    main()

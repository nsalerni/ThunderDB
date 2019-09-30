import os
from argparse import ArgumentParser
from thunderdb import thunderdb


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


def local_mode(data_file):
    """Run the key-value store on a single node in local mode (on your local machine, not in docker)
    """
    os.environ['NODE_ID'] = "0"
    os.environ['NODE_IP'] = "localhost"
    os.environ['NEXT_NODE_ID'] = "0"
    os.environ['NEXT_NODE_IP'] = "localhost"
    os.environ['DATA_FILE'] = data_file

    thunderdb.main()


def main(arguments):
    local_mode(arguments.data)


if __name__ == "__main__":
    main(parse_arguments())

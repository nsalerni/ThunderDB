## README

ThunderDB is a simple application to get started with, all you need are a few simple python dependencies and a data file to load the key-value store with. The README is split into two sections, one will cover how to get started with the single-node approach, and the other will cover how to run in distributed-mode, which requires an extra tool to simulate the other nodes.

## Single-Node 

### Python and Dependencies 

ThunderDB was developed using Python 3.7. Instructions for installing Python 3.7 on your OS are provided here: https://www.python.org/downloads/

If you are on a Mac, the easiest way to install Python 3.7 is by using homebrew.

```bash
# macOS (requirement homebrew - https://brew.sh/)
brew install python3
```

*Note: ThunderDB may work on Python 3.4, Python 3.5 and Python 3.6. Not all varients of Python 3.x have been validated.*

From the root of the package, run the following

```bash
# Install Python dependencies
pip install -r requirements.txt
```

### Running ThunderDB in Single-Node Mode

In order to run ThunderDB in single-node mode on your machine, please run the following script located in the root of the repo:

```bash
# Run in single-node mode with the path to the initial data file
# Example data files are located in ./sample_data/ in the root of the repo
python single_node_server.py --data sample_data/data_demo_small.txt
```

Once you start the server, you will be able to immediately make requests. *Note: please keep in mind that until your entire data file is loaded you may not be able to get specific results you are looking for.*

```bash
# GET request example: Looking for key="foo"
curl -i http://localhost:80/get/foo

# PUT request example: Adding example {"foo": "bar"}
curl -d '{"foo":"bar"}' -H "Content-Type:application/json" -X POST http://localhost:80/put

# SNAPSHOT request example: Dump all key-value pairs that exist on a node
curl -i http://localhost:80/snapshot
```

## Distributed-Nodes

In distributed-mode, we will rely on Docker to do the configuration and setup for us. Docker will also be responsible for setting up the nodes in our network, to easily simulate multiple nodes.

### Docker

The first step will be to install docker on your system. You can find the correct installation target from Docker's website: https://docs.docker.com/install/

#### Docker Quick Tips

``` bash
# Kill all docker containers
docker rm -f $(docker ps -aq)

# Kill a docker network, given its name
docker network rm <name_of_docker_network>
```

### Running ThunderDB in Distributed-Nodes Mode

Once you have docker installed, you are ready to start your distributed cluster in ThunderDB, which will use Docker to emulate multiple nodes on the network:

```bash
# Run in single-node mode with the path to the initial data file
# Example data files are located in ./sample_data/ in the root of the repo
# Since we are using Docker, any data file path must be relative to the project root as the directory will be mapped into Docker. 
./distributed_nodes_server.sh sample_data/data_deo_small.txt

# You can optionally pass an additional argument to get less or more nodes in your cluster (default: 3)
./distributed_nodes_server.sh sample_data/data_deo_small.txt 4
```

Once you start the server, you will be able to immediately make requests. *Note: please keep in mind that until your entire data file is loaded you may not be able to get specific results you are looking for.*

```bash
# GET request example: Looking for key="foo"
curl -i http://localhost:80/get/foo

# PUT request example: Adding example {"foo": "bar"}
curl -d '{"foo":"bar"}' -H "Content-Type:application/json" -X POST http://localhost:80/put

# SNAPSHOT request example: Dump all key-value pairs that exist on a node
curl -i http://localhost:80/snapshot

# You can also snapshot a node that is not the master node (localhost:80) 
# This allows you to see how the data was distributed with consistent hashing
curl -i http://localhost:81/snapshot
```

## Test Suite

In order to run our test suite, please run the following command from the project root:

```bash
python -m unittest tests/integ_test.py
```

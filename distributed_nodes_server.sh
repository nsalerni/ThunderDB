#!/bin/bash

if [[ -z $1 || ! -f $1 ]]; then
	echo "Usage: distributed_nodes_server.sh [data_file] [optional cluster size: default is 3]"
	echo "ERROR: Your data file path is invalid or you haven't specified a data file path"
  exit 1
fi

SERVICE="thunderdb"

# Build the docker image 
docker build -t "${SERVICE}" .

# Create a network for your docker containers
docker network create --subnet=172.19.0.0/16 thunderdb-network || true

NODE_ID=0 
LOCAL_PORT=80 
HOST_PREFIX="172.19.0.1"

NUM_NODES=${2:-3}

INFO_STRING="Starting cluster.. Master Node is accessible through localhost:80. The other nodes are available on localhost ports"

# Start each node in Docker
while [ ${NODE_ID} -lt ${NUM_NODES} ] 
do 
  node_ip="${HOST_PREFIX}${NODE_ID}"
  let next_node_id="(${NODE_ID} + 1) % ${NUM_NODES}"
  next_node_ip="${HOST_PREFIX}${next_node_id}"

  if [[ $((${NODE_ID} + 1)) -eq ${NUM_NODES} ]] 
  then 
    docker run --net thunderdb-network -p "${LOCAL_PORT}":80 --ip "${node_ip}" -e DATA_FILE="$1" -e NODE_ID="${NODE_ID}" -e NODE_IP="${node_ip}" -e NEXT_NODE_ID="${next_node_id}" -e NEXT_NODE_IP="${next_node_ip}" "${SERVICE}" & 
  fi 

  if [[ $((${NODE_ID} + 1)) -ne ${NUM_NODES} ]] 
  then 
    docker run --net thunderdb-network -p "${LOCAL_PORT}":80 --ip "${node_ip}" -e NODE_ID="${NODE_ID}" -e NODE_IP="${node_ip}" -e NEXT_NODE_ID="${next_node_id}" -e NEXT_NODE_IP="${next_node_ip}" "${SERVICE}" &
  fi

  INFO_STRING="${INFO_STRING} ${LOCAL_PORT}"
  
  NODE_ID=$((${NODE_ID} + 1))
  LOCAL_PORT=$((${LOCAL_PORT} + 1))
done

echo
echo "${INFO_STRING}"
echo

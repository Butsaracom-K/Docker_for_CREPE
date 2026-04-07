#!/bin/bash

docker ps -a

echo "--------------------"
echo "Type CONTAINER ID that you want to access here:"
read CONTAINER_ID
echo "--------------------"

docker start $CONTAINER_ID

docker exec -it $CONTAINER_ID bash

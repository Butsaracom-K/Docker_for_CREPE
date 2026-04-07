#!/bin/bash

docker build -t crepe_docker/ubuntu-22:v1 .

docker image ls
docker ps -a

echo "-------------------------"
echo "Next step: bash run-docker-after-build-image.sh"

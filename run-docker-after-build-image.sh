#!/bin/bash

docker images

echo "Please fill Image name of Docker"
read IMAGE

docker run -it $IMAGE bash

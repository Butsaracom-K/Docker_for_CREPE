#!/bin/bash

docker ps -a

echo '--------------------'
echo 'path here [pwd]:'
pwd
echo '--------------------'

echo 'Please enter the container_id here:'
read container_id
echo '--------------------'

echo 'Please Press Enter, if you want to copy the results here [pwd or other path]:'
read target_path


if [ -z "$target_path" ]; then
    target_path="."
fi

docker cp $container_id:/CREPE_Dir/CREPE/Results/ $target_path

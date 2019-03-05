#!/usr/bin/env bash

app_name="briteaccess"

running_docker_instances_names=$(docker ps -f name=${app_name} -f status=running -q 2> /dev/null )
number_running_docker_instances=$(echo "${running_docker_instances_names}" | wc -w )


echo "Instance names: ${running_docker_instances_names}"


if [[ ! number_running_docker_instances -eq 2 ]];
then
    echo ""
    echo "The docker containers are not running. Please, start with:"
    echo ""
    echo "docker-compose up -d"
    echo ""
    exit 1
fi

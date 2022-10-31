#!/bin/bash

eval $(minikube docker-env)
docker build -t eiachh/progression-manager ./
docker rmi $(docker images --filter "dangling=true" -q --no-trunc)
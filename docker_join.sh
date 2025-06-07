#!/bin/bash

CONTAINER_NAME=oop2025-dev

xhost +
docker exec -it \
    --privileged \
    -e DISPLAY=$DISPLAY \
    $CONTAINER_NAME \
    bash
xhost -

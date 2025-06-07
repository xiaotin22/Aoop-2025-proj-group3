#!/bin/bash

# 設定 container 名稱 & image 名稱
CONTAINER_NAME=oop-2025-proj-group10-dev
IMG_NAME=oop-2025-proj-group10-image:latest

# 專案根目錄
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# X11 授權檔案設定
XAUTH=/tmp/.docker.xauth
if [ ! -f $XAUTH ]; then
    xauth_list=$(xauth nlist $DISPLAY)
    if [ ! -z "$xauth_list" ]; then
        echo "$xauth_list" | sed -e 's/^..../ffff/' | xauth -f $XAUTH nmerge -
    else
        touch $XAUTH
    fi
    chmod a+r $XAUTH
fi
# 開啟 X11 存取
xhost +

# 檢查 image 是否已存在，否則建立
if ! docker image inspect "$IMG_NAME" > /dev/null 2>&1; then
    echo "Image not found, building: $IMG_NAME"
    docker build -t $IMG_NAME ./Docker
else
    echo "Docker image $IMG_NAME exists."
fi

# 檢查 container 是否已存在
if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    echo "Container exists, starting..."
    docker start -ai $CONTAINER_NAME
else
    echo "Creating and starting container..."
    docker run -it \
        --name $CONTAINER_NAME \
        -e DISPLAY=$DISPLAY \
        -e XAUTHORITY=$XAUTH \
        -v "$XAUTH:$XAUTH" \
        -v "$PROJECT_DIR:/home/arg/oop" \
        -v "/tmp/.X11-unix:/tmp/.X11-unix" \
        -w "/home/arg/oop" \
        --user root:root \
        --network host \
        --privileged \
        --security-opt seccomp=unconfined \
        $IMG_NAME \
        bash
fi

# 關閉 X11 存取
xhost -
#!/bin/bash

# 設定參數
CONTAINER_NAME=oop-2025-proj-group10-dev
IMG_NAME=oop-2025-proj-group10-image:latest
DOCKERFILE_DIR=./Docker
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
XAUTH=/tmp/.docker.xauth
USER_ID=$(id -u)
PULSE_SOCKET="/run/user/$USER_ID/pulse/native"

echo "🔧 [1/3] Building Docker image: $IMG_NAME ..."
docker build -t $IMG_NAME $DOCKERFILE_DIR
if [ $? -ne 0 ]; then
    echo "❌ Build failed. Exiting..."
    exit 1
fi

echo "🗑️ [2/3] Removing old container if it exists..."
docker rm -f $CONTAINER_NAME 2>/dev/null

# 建立 X11 授權檔案（for GUI）
if [ ! -f $XAUTH ]; then
    xauth_list=$(xauth nlist $DISPLAY)
    if [ ! -z "$xauth_list" ]; then
        echo "$xauth_list" | sed -e 's/^..../ffff/' | xauth -f $XAUTH nmerge -
    else
        touch $XAUTH
    fi
    chmod a+r $XAUTH
fi

# 檢查 XAUTH 是否建立成功
if [ ! -f $XAUTH ]; then
    echo "❌ [$XAUTH] was not properly created. Exiting..."
    exit 1
fi

echo "🚀 [3/3] Running container and entering bash..."
xhost +
docker run -it \
    --name $CONTAINER_NAME \
    -e DISPLAY=$DISPLAY \
    -e XAUTHORITY=$XAUTH \
    -e SDL_AUDIODRIVER=pulse \
    -e PULSE_SERVER=unix:/tmp/pulse/native \
    -v "$XAUTH:$XAUTH" \
    -v "$PROJECT_DIR:/root/oop" \
    -v "/tmp/.X11-unix:/tmp/.X11-unix" \
    -v "$PULSE_SOCKET:/tmp/pulse/native" \
    -w "/root/oop" \
    --user root:root \
    --network host \
    --privileged \
    --security-opt seccomp=unconfined \
    $IMG_NAME \
    bash
xhost -

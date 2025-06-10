#!/bin/bash

# === 參數設定 ===
CONTAINER_NAME=oop-2025-proj-group10-dev
IMG_NAME=oop-2025-proj-group10-image:latest
DOCKERFILE_DIR=./Docker
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
XAUTH=/tmp/.docker.xauth

# 自動抓主機的 UID / GID
HOST_UID=$(id -u)
HOST_GID=$(id -g)
PULSE_SOCKET="/run/user/$HOST_UID/pulse/native"

# === [1/3] 確認 image 是否存在 ===
if ! docker image inspect "$IMG_NAME" > /dev/null 2>&1; then
    echo "🔧 [1/3] Docker image not found. Building with UID=$HOST_UID and GID=$HOST_GID ..."
    docker build \
      --build-arg HOST_UID=$HOST_UID \
      --build-arg HOST_GID=$HOST_GID \
      -t $IMG_NAME $DOCKERFILE_DIR
    if [ $? -ne 0 ]; then
        echo "❌ Build failed. Exiting..."
        exit 1
    fi
else
    echo "✅ [1/3] Docker image $IMG_NAME already exists."
fi

# === [2/3] 移除舊 container（如果存在）===
echo "🗑️ [2/3] Removing old container if it exists..."
docker rm -f $CONTAINER_NAME 2>/dev/null

# === X11 授權設定 ===
if [ ! -f $XAUTH ]; then
    xauth_list=$(xauth nlist $DISPLAY)
    if [ ! -z "$xauth_list" ]; then
        echo "$xauth_list" | sed -e 's/^..../ffff/' | xauth -f $XAUTH nmerge -
    else
        touch $XAUTH
    fi
    chmod a+r $XAUTH
fi

if [ ! -f $XAUTH ]; then
    echo "❌ [$XAUTH] was not properly created. Exiting..."
    exit 1
fi

# === [3/3] 啟動 container ===
echo "🚀 [3/3] Running container and entering bash..."
xhost +
docker run -it \
    --name $CONTAINER_NAME \
    -e DISPLAY=$DISPLAY \
    -e XAUTHORITY=$XAUTH \
    -e SDL_AUDIODRIVER=pulse \
    -e PULSE_SERVER=unix:/tmp/pulse/native \
    -v "$XAUTH:$XAUTH" \
    -v "$PROJECT_DIR:/home/nycu/oop" \
    -v "/tmp/.X11-unix:/tmp/.X11-unix" \
    -v "$PULSE_SOCKET:/tmp/pulse/native" \
    -w "/home/nycu/oop" \
    --user nycu \
    --device /dev/snd \
    --network host \
    --privileged \
    --security-opt seccomp=unconfined \
    $IMG_NAME \
    bash
xhost -

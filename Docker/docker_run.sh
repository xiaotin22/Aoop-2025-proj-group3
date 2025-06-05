#!/bin/bash

# 設定 container 名稱
CONTAINER_NAME=oop-2025-group10

# 自動取得 repo 根目錄的絕對路徑
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 如果 container 已存在就進入它，否則新建一個並進入
if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    echo "Container exists, entering..."
    docker start -ai $CONTAINER_NAME
else
    echo "Creating and entering new container..."
    docker run -it --name $CONTAINER_NAME \
        -v "$PROJECT_DIR":/app \
        -w /app \
        --env DISPLAY=$DISPLAY \
        --network=host \
        -v /tmp/.X11-unix:/tmp/.X11-unix \
        xiaotin22/group10_project:latest \
        bash
fi
#!/bin/bash

# 設定 container 名稱 & image 名稱
CONTAINER_NAME=oop-2025-proj-group10-dev
IMG_NAME=oop-2025-proj-group10-image:latest

# 專案資料夾絕對路徑
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 嘗試建構 image（可以考慮加判斷是否已存在）
echo "🔧 Building image: $IMG_NAME"
docker build -t $IMG_NAME ./Docker

# 建立 X11 授權（給 GUI 用）
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

# 驗證 XAUTH 存在
if [ ! -f $XAUTH ]; then
    echo "❌ [$XAUTH] not properly created. Exiting..."
    exit 1
fi

# 開啟 X11 存取
xhost +

# 執行 Docker 容器
docker run -it --rm \
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

# 關閉 X11 存取
xhost -

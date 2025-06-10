#!/bin/bash

# === 設定參數 ===
CONTAINER_NAME=oop-2025-proj-group10-dev
IMG_NAME=oop-2025-proj-group10-image:latest
DOCKERFILE_DIR=./Docker
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
XAUTH=/tmp/.docker.xauth

# === 取得當前使用者 UID/GID 與 PulseAudio socket ===
USER_ID=$(id -u)
GROUP_ID=$(id -g)
PULSE_SOCKET="/run/user/$USER_ID/pulse/native"

# === 建立 X11 授權檔案（for GUI）===
if [ ! -f "$XAUTH" ]; then
    xauth_list=$(xauth nlist "$DISPLAY")
    if [ -n "$xauth_list" ]; then
        echo "$xauth_list" | sed -e 's/^..../ffff/' | xauth -f "$XAUTH" nmerge -
    else
        touch "$XAUTH"
    fi
    chmod a+r "$XAUTH"
fi

# === 檢查 XAUTH 是否建立成功 ===
if [ ! -f "$XAUTH" ]; then
    echo "❌ [$XAUTH] was not properly created. Exiting..."
    exit 1
fi

# === 啟用 X11 存取權限 ===
xhost +

# === 檢查 image 是否存在，否則重新 build（含 UID/GID）===
if ! docker image inspect "$IMG_NAME" > /dev/null 2>&1; then
    echo "🛠️ Image not found, building: $IMG_NAME"
    docker build \
        --build-arg HOST_UID="$USER_ID" \
        --build-arg HOST_GID="$GROUP_ID" \
        -t "$IMG_NAME" "$DOCKERFILE_DIR"
else
    echo "✅ Docker image $IMG_NAME exists."
fi

# === 移除舊 container（保證乾淨）===
docker rm -f "$CONTAINER_NAME" 2>/dev/null

# === 啟動 container ===
echo "🚀 Starting container with GUI + audio support..."
docker run -it \
    --name "$CONTAINER_NAME" \
    -e DISPLAY="$DISPLAY" \
    -e SDL_AUDIODRIVER=pulse \
    -e PULSE_SERVER=unix:/tmp/pulse/native \
#!/bin/bash

# === 設定參數 ===
CONTAINER_NAME=oop-2025-proj-group10-dev
IMG_NAME=oop-2025-proj-group10-image:latest
DOCKERFILE_DIR=./Docker
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
XAUTH=/tmp/.docker.xauth

# === 取得當前使用者 UID/GID 與 PulseAudio socket ===
USER_ID=$(id -u)
GROUP_ID=$(id -g)
PULSE_SOCKET="/run/user/$USER_ID/pulse/native"

# === 建立 X11 授權檔案（for GUI）===
if [ ! -f "$XAUTH" ]; then
    xauth_list=$(xauth nlist "$DISPLAY")
    if [ -n "$xauth_list" ]; then
        echo "$xauth_list" | sed -e 's/^..../ffff/' | xauth -f "$XAUTH" nmerge -
    else
        touch "$XAUTH"
    fi
    chmod a+r "$XAUTH"
fi

# === 檢查 XAUTH 是否建立成功 ===
if [ ! -f "$XAUTH" ]; then
    echo "❌ [$XAUTH] was not properly created. Exiting..."
    exit 1
fi

# === 啟用 X11 存取權限 ===
xhost +

# === 檢查 image 是否存在，否則重新 build（含 UID/GID）===
if ! docker image inspect "$IMG_NAME" > /dev/null 2>&1; then
    echo "🛠️ Image not found, building: $IMG_NAME"
    docker build \
        --build-arg HOST_UID="$USER_ID" \
        --build-arg HOST_GID="$GROUP_ID" \
        -t "$IMG_NAME" "$DOCKERFILE_DIR"
else
    echo "✅ Docker image $IMG_NAME exists."
fi

# === 移除舊 container（保證乾淨）===
docker rm -f "$CONTAINER_NAME" 2>/dev/null

# === 啟動 container ===
echo "🚀 Starting container with GUI + audio support..."
docker run -it \
    --name "$CONTAINER_NAME" \
    -e DISPLAY="$DISPLAY" \
    -e SDL_AUDIODRIVER=pulse \
    -e PULSE_SERVER=unix:/tmp/pulse/native \#!/bin/bash

# === 設定參數 ===
CONTAINER_NAME=oop-2025-proj-group10-dev
IMG_NAME=oop-2025-proj-group10-image:latest
DOCKERFILE_DIR=./Docker
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
XAUTH=/tmp/.docker.xauth

# === 取得當前使用者 UID/GID 與 PulseAudio socket ===
USER_ID=$(id -u)
GROUP_ID=$(id -g)
PULSE_SOCKET="/run/user/$USER_ID/pulse/native"

# === 建立 X11 授權檔案（for GUI）===
if [ ! -f "$XAUTH" ]; then
    xauth_list=$(xauth nlist "$DISPLAY")
    if [ -n "$xauth_list" ]; then
        echo "$xauth_list" | sed -e 's/^..../ffff/' | xauth -f "$XAUTH" nmerge -
    else
        touch "$XAUTH"
    fi
    chmod a+r "$XAUTH"
fi

# === 檢查 XAUTH 是否建立成功 ===
if [ ! -f "$XAUTH" ]; then
    echo "❌ [$XAUTH] was not properly created. Exiting..."
    exit 1
fi

# === 啟用 X11 存取權限 ===
xhost +

# === 檢查 image 是否存在，否則重新 build（含 UID/GID）===
if ! docker image inspect "$IMG_NAME" > /dev/null 2>&1; then
    echo "🛠️ Image not found, building: $IMG_NAME"
    docker build \
        --build-arg HOST_UID="$USER_ID" \
        --build-arg HOST_GID="$GROUP_ID" \
        -t "$IMG_NAME" "$DOCKERFILE_DIR"
else
    echo "✅ Docker image $IMG_NAME exists."
fi

# === 移除舊 container（保證乾淨）===
docker rm -f "$CONTAINER_NAME" 2>/dev/null

# === 啟動 container ===
echo "🚀 Starting container with GUI + audio support..."
docker run -it \
    --name "$CONTAINER_NAME" \
    -e DISPLAY="$DISPLAY" \
    -e SDL_AUDIODRIVER=pulse \
    -e PULSE_SERVER=unix:/tmp/pulse/native \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v "$XAUTH:$XAUTH" \
    -e XAUTHORITY=$XAUTH \
    -v "$PULSE_SOCKET:/tmp/pulse/native" \
    -v "$PROJECT_DIR:/home/dev/project" \
    "$IMG_NAME"
FROM python:3.13

# 取得 Host 傳進來的 UID / GID
ARG HOST_UID
ARG HOST_GID

# 安裝必要套件
RUN apt update && apt install -y \
    x11-apps \
    python3-tk \
    libgl1 \
    libpulse0 \
    && rm -rf /var/lib/apt/lists/*

# 建立對應使用者
RUN groupadd -g $HOST_GID nycugroup && \
    useradd -m -u $HOST_UID -g nycugroup nycu

# 設定工作目錄 & 安裝 Python 套件
WORKDIR /home/nycu/oop
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# 設定環境變數（音效）
ENV SDL_AUDIODRIVER=pulse
ENV PULSE_SERVER=unix:/tmp/pulse/native

# 預設切換到使用者（可選）
USER nycu

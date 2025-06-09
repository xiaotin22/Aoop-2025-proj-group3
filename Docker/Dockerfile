FROM python:3.13

# 安裝常用工具 & GUI 套件（依課程需求加）
RUN apt update && apt install -y \
    x11-apps \
    python3-tk \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# 設定工作目錄
WORKDIR /root/oop

# 複製 requirements 並安裝
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN apt-get update && apt-get install -y libpulse0


ENV SDL_AUDIODRIVER=pulse
ENV PULSE_SERVER=unix:/tmp/pulse/native


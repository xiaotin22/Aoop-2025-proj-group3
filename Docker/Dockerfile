# 使用 Python 3.11 的精簡版本
FROM python:3.11-slim

# 安裝一些常用工具與 pygame 依賴
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    && rm -rf /var/lib/apt/lists/*

    
# 設定容器內的預設工作目錄
WORKDIR /app

# 複製 Python 套件清單並安裝
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
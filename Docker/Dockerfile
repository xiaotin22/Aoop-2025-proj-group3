FROM python:3.13

# 安裝常用工具 & GUI 套件（依課程需求加）
RUN apt update && apt install -y \
    x11-apps \
    python3-tk \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# 建立使用者（與 run.sh 中一致）
RUN useradd -ms /bin/bash arg

# 設定工作目錄
WORKDIR /home/nycu

# 複製 requirements 並安裝
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# 預設使用 nycu 使用者
USER nycu
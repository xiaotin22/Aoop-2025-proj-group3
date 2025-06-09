# OOP 2025 Group 10 Project

**本專案為 113-2 陽明交通大學（NYCU）由王學誠老師開設的物件導向程式設計（OOP）課程的期末成果，主要在練習使用 Python, Pygame的一些函式庫** 

我們的組員如下 Group10： 
* NYCU_EE [113511116 tpvupu](https://github.com/tpvupu) : 陳欣怡
* NYCU_EE [113511203 calistayang](https://github.com/calistayang)：楊馨惠
* NYCU_EE [113511266 xiaotin22](https://github.com/xiaotin22)：楊庭瑞

## 📂 專案架構 (Project Structure)
---

## 🛠️ 安裝與執行 (Getting Started)

如果想要在自己的本機執行這個遊戲，請依照下列步驟執行呦～

### 必要條件

* Python 3.13 (為確保與部署環境一致，建議使用此版本)
* Git
  
### 安裝步驟

1.  **Clone 專案庫**
    ```bash
    git clone https://github.com/xiaotin22/oop-2025-proj-group10.git
    cd oop-2025-proj-group10
    ```

2.  **建立並啟用虛擬環境 (強烈建議)**
    * 在 Windows 上:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    * 在 macOS / Linux 上:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **安裝相依套件**
    ```bash
    pip install -r Docker/requirements.txt
    ```

4.  **執行遊戲！**
    ```bash
    python main.py
    ```
---



# About Our Docker (現在有音效無法播放的問題，先不要用)🚀

🧰 前置需求（第一次才需要）

### Step1 : 安裝 Docker (如果沒有裝過的話)  
   [👉 Docker 官方下載連結](https://www.docker.com/products/docker-desktop)

### Step2: Clone 這個 repo 到你的電腦：
```
cd ~
git clone https://github.com/xiaotin22/oop-2025-proj-group10.git
cd oop-2025-proj-group10
```
### Step3: 進入Docker
```
source docker_run.sh
```

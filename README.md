# OOP 2025 Group 10 Project

**本專案為 113-2 陽明交通大學（NYCU）由王學誠老師開設的物件導向程式設計（OOP）課程的期末成果，主要在練習使用 Python, Pygame的一些函式庫** 

我們的組員如下 Group10： 
* NYCU_EE [113511116 tpvupu](https://github.com/tpvupu) : 陳欣怡
* NYCU_EE [113511203 calistayang](https://github.com/calistayang)：楊馨惠
* NYCU_EE [113511266 xiaotin22](https://github.com/xiaotin22)：楊庭瑞

## 📂 專案架構 (Project Structure)
``` bash
oop-2025-proj-group10/
│
├── main.py                      # 主程式入口，負責遊戲流程控制
├── character.py                 # 角色類別與屬性、行為邏輯
├── simulation.py                # 用以模擬隨機選擇結果
│
├── UI/
│   ├── intro_scene.py           # 遊戲開場動畫/說明場景
│   ├── main_scene.py            # 遊戲主畫面場景
│   ├── story_scene.py           # 劇情推進場景
│   ├── event_scene.py           # 事件觸發場景
│   ├── attribute_scene.py       # 角色屬性顯示場景
│   ├── character_select.py      # 角色選擇場景
│   ├── end_scene.py             # 遊戲結束/結局場景
│   ├── sound_control_scene.py   # 音效/音樂控制場景
│   ├── lucky_wheel_scene.py     # 幸運轉盤小遊戲
│   └── components/
│       ├── audio_manager.py      # 音效/音樂管理單例
│       ├── base_scene.py         # 場景基底類別
│       ├── character_animator.py # 角色動畫管理
│       └── ...                   # 其他 UI 元件
│
├── simulation_plots/            # 模擬成績繪製圖形存放
│
├── resource/
│   ├── font/                    # 字型檔案
│   ├── image/                   # 圖片、背景、角色圖
│   └── music/
│       ├── bgm/                 # 背景音樂
│       └── sound_effect/        # 音效檔案
│
├── event/
│   └── event.json               # 各週事件資料
│
├── README.md                    # 專案說明文件
├── game_setting/                # 遊戲劇情總述
│      └── ...
├── Docker/
```
---

## 🛠️ 安裝與執行 (Getting Started)

如果想要在自己的本機執行這個遊戲，請依照下列步驟執行呦～

### 必要條件

* Python 3.13 (建議）
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



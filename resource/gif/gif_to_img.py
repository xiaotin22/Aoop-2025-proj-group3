# gif_to_img.py
# 這個程式會將 GIF 檔案分解成多張圖片，並建立一個同檔名的資料夾來存放這些圖片。
# 你可以修改 TARGET_GIF 變數來指定你自己的 GIF 檔案

from PIL import Image
import os
import pygame

def gif_to_img(source_gif=None):
    # 自動取得 gif 的完整路徑
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Target GIF 
    TARGET_GIF = os.path.join(current_dir, source_gif)
    # 取得 base 名稱與目標資料夾
    base_name = os.path.splitext(os.path.basename(TARGET_GIF))[0]
    frames_dir = os.path.join(current_dir, f"{base_name}_frames")
    os.makedirs(frames_dir, exist_ok=True)

    # 開始分解 GIF
    gif = Image.open(TARGET_GIF)
    frame_count = 0

    try:
        while True:
            gif.seek(frame_count)
            gif.save(os.path.join(frames_dir, f"frame_{frame_count}.png"))
            frame_count += 1
    except EOFError:
        print(f"✅ 共分解 {frame_count} 張 frames 存到資料夾：{frames_dir}")


if __name__ == "__main__":
    # 測試 gif_to_img 函式
    # 這裡可以修改為你自己的 GIF 檔案名稱
    gif_to_img("mitao_intro.gif")

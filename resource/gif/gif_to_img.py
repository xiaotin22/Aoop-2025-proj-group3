from PIL import Image
import os
import pygame

# gif_to_img.py
# 這個程式會將 GIF 檔案分解成多張圖片，並存到指定的資料夾中
# This is the code to decompose a GIF file into multiple images and save them in a new folder with their names
# You can modify the TARGET_GIF variable to point to your own GIF file


# 自動取得 gif 的完整路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
# Target GIF 檔案的路徑可修改為你自己的 GIF 檔案
TARGET_GIF = os.path.join(current_dir, "bubu_lying.gif")

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


# 用於載入 frames 的函式
def load_frames(folder_path):
    frames = []
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(".png"):
            frame_path = os.path.join(folder_path, filename)
            img = pygame.image.load(frame_path).convert_alpha()
            frames.append(img)
    return frames


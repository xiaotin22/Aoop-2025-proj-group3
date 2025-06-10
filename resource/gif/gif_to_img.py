# gif_to_img.py
# 這個程式會將目錄下的所有 GIF 檔案分解成多張圖片，並各自存到對應的資料夾中。

from PIL import Image
import os

def gif_to_img(source_gif):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    TARGET_GIF = os.path.join(current_dir, source_gif)

    base_name = os.path.splitext(os.path.basename(TARGET_GIF))[0]
    frames_dir = os.path.join(current_dir, f"{base_name}_frames")
    os.makedirs(frames_dir, exist_ok=True)

    gif = Image.open(TARGET_GIF)
    frame_count = 0

    try:
        while True:
            gif.seek(frame_count)
            gif.save(os.path.join(frames_dir, f"frame_{frame_count}.png"))
            frame_count += 1
    except EOFError:
        print(f"✅ {source_gif} 共分解 {frame_count} 張 frames，已存到資料夾：{frames_dir}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    gif_files = [f for f in os.listdir(current_dir) if f.lower().endswith(".gif")]

    if not gif_files:
        print("😥 找不到任何 .gif 檔案喔！")
    else:
        print(f"🔍 發現 {len(gif_files)} 個 GIF 檔案，開始處理...")
        for gif_file in gif_files:
            gif_to_img(gif_file)
        print("🎉 所有 GIF 都處理完成啦！")

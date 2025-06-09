import pygame
import os

# === 初始化 Pygame ===
pygame.init()
screen = pygame.display.set_mode((400, 400))  # 調整視窗大小
pygame.display.set_caption("播放 bubu_lying 動畫")
clock = pygame.time.Clock()

# === 載入所有 frames ===
frames = []
frames_dir = os.path.join("resource", "gif", "bubu_lying_frames")
for filename in sorted(os.listdir(frames_dir)):
    if filename.endswith(".png"):
        frame_path = os.path.join(frames_dir, filename)
        image = pygame.image.load(frame_path).convert_alpha()
        frames.append(image)

# === 動畫參數 ===
frame_index = 0
frame_delay = 100  # 每張圖持續時間（毫秒）
last_update = pygame.time.get_ticks()

# === 主迴圈 ===
running = True
while running:
    now = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 更新 frame（動畫換圖）
    if now - last_update > frame_delay:
        frame_index = (frame_index + 1) % len(frames) # 循環播放 frames
        last_update = now  

    # 畫面更新
    screen.fill((255, 255, 255))  # 清空背景
    screen.blit(frames[frame_index], (100, 100))  # 畫在座標 (100, 100)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

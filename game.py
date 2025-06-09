import resource.gif.gif_to_img as gif_to_img # Ensure the GIF frames are extracted before running this script
import pygame
import os

#define param 
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 800

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Bubu Lying Animation Test')  

clock = pygame.time.Clock()

# === 載入所有 frames ===
bubu_frames = gif_to_img.load_frames("resource/gif/bubu_lying_frames")

# === 初始化參數 ===
bubu_index = 0
yier_index = 0
frame_delay = 100  # 每幀間隔時間（毫秒）
last_update_bubu = pygame.time.get_ticks()
last_update_yier = pygame.time.get_ticks()

# === 主迴圈 ===
running = True
while running:
    now = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 更新 bubu 動畫
    if now - last_update_bubu > frame_delay:
        bubu_index = (bubu_index + 1) % len(bubu_frames)
        last_update_bubu = now

    # 畫面更新
    screen.fill((255, 255, 255))
    screen.blit(bubu_frames[bubu_index], (100, 150))  # 左邊
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
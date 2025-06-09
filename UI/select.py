import pygame
import os

def load_frames(folder_path):
    frames = []
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(".png"):
            img = pygame.image.load(os.path.join(folder_path, filename)).convert_alpha()
            frames.append(img)
    return frames

# --- 初始化 ---
SCREEN_HEIGHT = 800
SCREEN_WIDTH = 1200
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Select Character')
clock = pygame.time.Clock()
FPS = 30

# 音樂播放
pygame.mixer.music.load('../resource/music/bgm/yier_bubu.mp3')
pygame.mixer.music.play(-1)

# 載入圖片
bubu_frames = load_frames("../resource/gif/bubu_intro_frames")
yier_frames = load_frames("../resource/gif/yier_intro_frames")
mitao_frames = load_frames("../resource/gif/mitao_intro_frames")
huihui_frames = load_frames("../resource/gif/huihui_intro_frames")

# 幀控制
frame_index = 0

# 框框大小
box_width = 300
box_height = 300
margin = 50  # 邊界距離

# 四個框框位置（左上、右上、左下、右下）
box_positions = [
    (margin, margin),  # bubu 左上
    (SCREEN_WIDTH - margin - box_width, margin),  # yier 右上
    (margin, SCREEN_HEIGHT - margin - box_height),  # mitao 左下
    (SCREEN_WIDTH - margin - box_width, SCREEN_HEIGHT - margin - box_height)  # huihui 右下
]

# --- 主迴圈 ---
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 更新動畫索引
    if pygame.time.get_ticks() % (1000 // FPS * 5) < (1000 // FPS):
        frame_index = (frame_index + 1) % len(bubu_frames)

    screen.fill((255, 255, 255))  # 背景白色

    # 畫框框 + 顯示角色
    pygame.draw.rect(screen, (0, 0, 0), (*box_positions[0], box_width, box_height), 5)
    screen.blit(bubu_frames[frame_index], (box_positions[0][0] + 30, box_positions[0][1] + 30))

    pygame.draw.rect(screen, (0, 0, 0), (*box_positions[1], box_width, box_height), 5)
    screen.blit(yier_frames[frame_index], (box_positions[1][0] + 30, box_positions[1][1] + 30))

    pygame.draw.rect(screen, (0, 0, 0), (*box_positions[2], box_width, box_height), 5)
    screen.blit(mitao_frames[frame_index], (box_positions[2][0] + 30, box_positions[2][1] + 30))

    pygame.draw.rect(screen, (0, 0, 0), (*box_positions[3], box_width, box_height), 5)
    screen.blit(huihui_frames[frame_index], (box_positions[3][0] + 30, box_positions[3][1] + 30))

    pygame.display.flip()

pygame.quit()

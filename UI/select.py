#遊戲開始的選擇介面
import pygame
import os
from resource.gif.gif_to_img import load_frames
# 定義參數
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 800
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Select Character')

# 載入音樂
pygame.mixer.music.load('resource/music/Mitao_Huihui.mp3')
pygame.mixer.music.play(-1)  # -1 means loop indefinitely

# 載入角色選擇的圖片
current_dir = os.path.dirname(os.path.abspath(__file__))
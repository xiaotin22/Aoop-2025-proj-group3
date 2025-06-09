import pygame
import os
from UI.start_select import CharacterSelectScene

pygame.init()
# Define screen dimensions
SCREEN_HEIGHT = 800
SCREEN_WIDTH = 1200
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption('Game Start')

scene = CharacterSelectScene(screen)
selected_character = scene.run()

print("玩家選擇角色為：", selected_character)
pygame.quit()

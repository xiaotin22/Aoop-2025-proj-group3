import pygame


#define param 
SCREEN_HEIGHT = 900
SCREEN_WIDTH = 1600

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('00_EmptyWindow')

#add music
pygame.mixer.music.load('resource/music/Mitao_Huihui.mp3')
pygame.mixer.music.play(-1)  # -1 means loop indefinitely


#game loop
is_runnung = True
while is_runnung:
    screen.fill((255, 255, 255))
    #event handler
    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            is_runnung = False
    pygame.display.update()
pygame.quit()
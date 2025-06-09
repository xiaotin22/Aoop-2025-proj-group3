import pygame
pygame.mixer.init()
sound = pygame.mixer.Sound("resource/music/sound_effect/menu_hover.mp3")
sound.play()
input("Press Enter to quit...")

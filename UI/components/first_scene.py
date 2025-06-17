import pygame
import asyncio

class FirstScene:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        
    def run(self):
        self.running = True
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN, pygame.FINGERDOWN):
                    # 使用者互動，結束 FirstScene
                    return "START"
            # 畫黑幕
            self.screen.fill((0, 0, 0))
            
            pygame.display.flip()
            
            clock.tick(60)
import pygame

class BaseScene:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.SCREEN_HEIGHT = 800
        self.SCREEN_WIDTH = 1200
        self.clock = pygame.time.Clock()
        self.FPS = 30
        self.hover_sound = pygame.mixer.Sound("resource/music/sound_effect/menu_hover.mp3")

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False

    def update(self):
        pass  # 由子類別實作

    def draw(self):
        pass  # 由子類別實作

    def run(self):
        while self.running:
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(self.FPS) 
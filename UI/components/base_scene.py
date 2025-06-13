import pygame
import os

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

    def load_frames(self, folder_path):
        frames = []
        for filename in sorted(os.listdir(folder_path)):
            if filename.endswith(".png"):
                img = pygame.image.load(os.path.join(folder_path, filename)).convert_alpha()
                img = pygame.transform.scale(img, self.char_size)
                frames.append(img)
        return frames
    
def wrap_text(text, font, max_width):
    lines = []
    paragraphs = text.split('\n')  # 支援多段落

    for para in paragraphs:
        current_line = ""
        for char in para:
            test_line = current_line + char
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = char
        if current_line:
            lines.append(current_line)

    return lines

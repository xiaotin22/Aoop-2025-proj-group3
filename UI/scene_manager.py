import pygame
import os
class SceneManager:
    def __init__(self, start_scene):
        self.current_scene = start_scene

    def switch_to(self, new_scene):
        self.current_scene = new_scene

    def update(self):
        if self.current_scene:
            self.current_scene.update()

    def draw(self, screen):
        if self.current_scene:
            self.current_scene.draw(screen)

    def handle_event(self, event):
        if self.current_scene:
            self.current_scene.handle_event(event)
            
class Scene:
    def __init__(self, screen):
        self.screen = screen
        self.SCREEN_HEIGHT = 800
        self.SCREEN_WIDTH = 1200
        self.clock = pygame.time.Clock()
        self.FPS = 30
        self.running = True
        self.font = pygame.font.Font("resource/font/JasonHandwriting3-SemiBold.ttf", 36)
        self.font_desc = pygame.font.Font("resource/font/JasonHandwriting3-Regular.ttf", 28)
        self.hover_sound = pygame.mixer.Sound("resource/music/sound_effect/menu_hover.mp3")
        self.char_size = (140, 140)

        # 背景圖片
        self.background = pygame.image.load("resource/image/background_intro.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, self.screen.get_size())
        self.background.set_alpha(100)
    
    def load_frames(self, folder_path):
        frames = []
        for filename in sorted(os.listdir(folder_path)):
            if filename.endswith(".png"):
                img = pygame.image.load(os.path.join(folder_path, filename)).convert_alpha()
                img = pygame.transform.scale(img, self.char_size)
                frames.append(img)
        return frames
    
    def wrap_text(self, text, font, max_width):
        lines = []
        paragraphs = text.split('\n')  # 先根據 \n 分段

        for para in paragraphs:
            words = para.split(' ')
            current_line = ""
            for word in words:
                test_line = f"{current_line} {word}".strip()
                if font.size(test_line)[0] <= max_width:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)
        
        return lines

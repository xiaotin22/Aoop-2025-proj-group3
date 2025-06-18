import pygame
from UI.components.audio_manager import AudioManager
import setting

class ImageButton:
    def __init__(self, image_path, pos, size=None, text="", font=None, text_color=(50, 50, 50), hover_scale=1.1):
        self.audio = AudioManager.get_instance()
        self.image_original = pygame.image.load(image_path).convert_alpha()
        if size:
            self.image_original = pygame.transform.smoothscale(self.image_original, size)
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect(topleft=pos)
        self.center = self.rect.center  # 記錄中心點，縮放時用
        self.text = text
        self.font = font
        self.text_color = text_color
        self.is_hover = False
        self.hover_scale = hover_scale
        self.hover_sound_played = False
        self.mask = pygame.mask.from_surface(self.image_original)

        # 若有文字，預先渲染
        if self.text and self.font:
            self.text_surface = self.font.render(self.text, True, self.text_color)
            self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        else:
            self.text_surface = None

    def is_mouse_on_button(self, mouse_pos):
        rel_x = mouse_pos[0] - self.rect.left
        rel_y = mouse_pos[1] - self.rect.top
        if 0 <= rel_x < self.rect.width and 0 <= rel_y < self.rect.height:
            return self.mask.get_at((int(rel_x), int(rel_y)))
        return False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_mouse_on_button(event.pos):
                return True
        return False

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        prev_hover = self.is_hover
        self.is_hover = self.is_mouse_on_button(mouse_pos)

        if self.is_hover and not prev_hover:
            self.audio.play_sound(setting.SoundEffect.MENU_HOVER_PATH)

        self.update_hover()

    def update_hover(self):
        if self.is_hover:
            scaled_size = (
                int(self.image_original.get_width() * self.hover_scale),
                int(self.image_original.get_height() * self.hover_scale)
            )
            self.image = pygame.transform.smoothscale(self.image_original, scaled_size)
            self.rect = self.image.get_rect(center=self.center)
            self.mask = pygame.mask.from_surface(self.image)  # <--- 這裡重建 mask
            if self.text_surface:
                self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        else:
            self.image = self.image_original
            self.rect = self.image.get_rect(center=self.center)
            self.mask = pygame.mask.from_surface(self.image)  # <--- 這裡重建 mask
            if self.text_surface:
                self.text_rect = self.text_surface.get_rect(center=self.rect.center)


    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.text_surface:
            screen.blit(self.text_surface, self.text_rect)

    def is_clicked(self, event):
        return self.handle_event(event)
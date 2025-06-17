import pygame
from UI.components.audio_manager import AudioManager

class ImageButton:
    def __init__(self, image_path, pos, size=None, text="", font=None, text_color=(50, 50, 50)):
        self.image_original = pygame.image.load(image_path).convert_alpha()
        if size:
            self.image_original = pygame.transform.smoothscale(self.image_original, size)
        self.image = self.image_original
        self.rect = self.image.get_rect(topleft=pos)

        self.text = text
        self.font = font
        self.text_color = text_color

        self.hover_scale = 1.1
        self.is_hover = False
        self.scale = 1.0

        self.hover_sound_played = False  # 👈 用來避免一直播
        self.audio = AudioManager.get_instance()  # 👈 取得音效控制器
        self.hover_sound_path = "resource/music/sound_effect/menu_hover.MP3"  # 可以設定預設 hover 音效

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hover = self.rect.collidepoint(event.pos)
            self.update_hover()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def update_hover(self):
        if self.is_hover:
            scaled_size = (
                int(self.image_original.get_width() * self.hover_scale),
                int(self.image_original.get_height() * self.hover_scale)
            )
            self.image = pygame.transform.smoothscale(self.image_original, scaled_size)
            self.rect = self.image.get_rect(center=self.rect.center)
        else:
            self.image = self.image_original
            self.rect = self.image.get_rect(topleft=self.rect.topleft)


    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if not self.hover_sound_played:
                self.audio.play_sound(self.hover_sound_path)
                self.hover_sound_played = True
            if not self.is_hover:
                self.is_hover = True
                w, h = self.image_original.get_size()
                self.image = pygame.transform.smoothscale(
                    self.image_original,
                    (int(w * self.hover_scale), int(h * self.hover_scale))
                )
                self.rect = self.image.get_rect(center=self.rect.center)
        else:
            self.hover_sound_played = False
            if self.is_hover:
                self.image = self.image_original
                self.rect = self.image.get_rect(center=self.rect.center)
                self.is_hover = False

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        if self.text and self.font:
            text_surf = self.font.render(self.text, True, self.text_color)
            text_rect = text_surf.get_rect(center=self.rect.center)
            screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        return self.rect.collidepoint(event.pos)
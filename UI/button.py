import pygame
from abc import ABC, abstractmethod

class BaseButton(ABC):
    def __init__(self, action=None, font=None, text="", icon=None, hover_sound=None, style=None):
        self.action = action
        self.font = font
        self.text = text
        self.icon = icon
        self.hover_sound = hover_sound
        self.style = style
        self.hover = False
        self.hovered_last = False
        self.scale = 1.0

    @abstractmethod
    def update(self, mouse_pos): pass

    @abstractmethod
    def draw(self, screen): pass

    @abstractmethod
    def is_clicked(self, mouse_pos): pass
    
class RectButton(BaseButton):
    def __init__(self, pos, size, **kwargs):
        super().__init__(**kwargs)
        self.rect = pygame.Rect(pos, size)

    def update(self, mouse_pos):
        self.hover = self.rect.collidepoint(mouse_pos)
        target_scale = 1.1 if self.hover else 1.0
        self.scale += (target_scale - self.scale) * 0.2

        if self.hover and not self.hovered_last and self.hover_sound:
            self.hover_sound.play()
        self.hovered_last = self.hover

    def draw(self, screen):
        scaled_w = int(self.rect.width * self.scale)
        scaled_h = int(self.rect.height * self.scale)
        scaled_rect = pygame.Rect(0, 0, scaled_w, scaled_h)
        scaled_rect.center = self.rect.center

        color = self.style.hover_color if self.hover else self.style.base_color
        if not self.style.transparent:
            pygame.draw.rect(screen, color, scaled_rect, border_radius=self.style.border_radius)
            pygame.draw.rect(screen, self.style.border_color, scaled_rect, 2, border_radius=self.style.border_radius)

        if self.icon:
            icon_rect = self.icon.get_rect()
            icon_rect.centery = scaled_rect.centery
            icon_rect.left = scaled_rect.left + 15
            screen.blit(self.icon, icon_rect)
        else:
            icon_rect = None

        if self.font and self.text:
            text_surface = self.font.render(self.text, True, self.style.text_color)
            text_rect = text_surface.get_rect()
            text_rect.centery = scaled_rect.centery
            text_rect.left = icon_rect.right + 10 if self.icon else scaled_rect.centerx - text_rect.width // 2
            screen.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    
    


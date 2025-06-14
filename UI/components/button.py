import pygame
from UI.components.base_scene import  wrap_text, draw_wrapped_text

class Button:
    def __init__(self, x, y, width, height, text, font,
                 bg_color=(200, 180, 150), 
                 text_color=(50, 30, 10),
                 hover_color=(255, 220, 180),
                 border_radius=8, font_size=36 ):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font  
        self.bg_color = bg_color
        self.text_color = text_color
        self.hover_color = hover_color
        self.border_radius = border_radius
        self.is_hovered = False
        self.font_size = font_size
        self.width = width
        self.height = height
        
        try:
            self.hover_sound = pygame.mixer.Sound("resource/music/sound_effect/menu_hover.mp3")
        except Exception:
            self.hover_sound = None

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.bg_color
        
        pygame.draw.rect(surface, color, self.rect, border_radius=self.border_radius)
        
        draw_wrapped_text(surface, self.text, self.font, self.rect)
        

    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        was_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        if self.is_hovered and not was_hovered and self.hover_sound:
            self.hover_sound.play()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            return True
        return False

    def set_text(self, new_text):
        self.text = new_text

    def set_position(self, x, y):
        self.rect.topleft = (x, y)

    def set_size(self, width, height):
        self.rect.size = (width, height)

    def set_color(self, bg_color=None, text_color=None, hover_color=None):
        if bg_color:
            self.bg_color = bg_color
        if text_color:
            self.text_color = text_color
        if hover_color:
            self.hover_color = hover_color
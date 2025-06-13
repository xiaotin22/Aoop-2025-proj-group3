import pygame
from components.base_scene import  wrap_text

class Button:
    def __init__(self, x, y, width, height, text, font_path,
                 bg_color=(200, 180, 150), 
                 text_color=(50, 30, 10),
                 hover_color=(255, 220, 180),
                 border_radius=8, font_size=36 ):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font_path = font_path or pygame.font.Font("resource/font/JasonHandwriting3-SemiBold.ttf", 36)
        self.bg_color = bg_color
        self.text_color = text_color
        self.hover_color = hover_color
        self.border_radius = border_radius
        self.is_hovered = False
        self.font_size = font_size
        
        try:
            self.hover_sound = pygame.mixer.Sound("resource/music/sound_effect/menu_hover.mp3")
        except Exception:
            self.hover_sound = None

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.bg_color
        
        pygame.draw.rect(surface, color, self.rect, border_radius=self.border_radius)
        
        lines = wrap_text( self.text, self.font, self.width - 20 )
        line_height = self.font_size + 5  # font size for small font
        total_height = line_height * len(lines)
        start_y = self.rect.top + (self.rect.height - total_height) // 2

    
        for i, line in enumerate(lines):
            txt_surf = self.font_path.render(line, True, self.text_color)
            txt_rect = txt_surf.get_rect()
            txt_rect.left = self.rect.left + 10
            txt_rect.top = start_y + i * line_height
            surface.blit(txt_surf, txt_rect)

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
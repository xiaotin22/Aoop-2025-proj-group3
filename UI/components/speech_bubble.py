import pygame

class SpeechBubble:
    def __init__(self, text, pos, font, duration=1500):
        self.text = text
        self.pos = pos  # (x, y) 中心點
        self.font = font
        self.start_time = pygame.time.get_ticks()
        self.duration = duration  # 毫秒

    def draw(self, screen):
        text_surf = self.font.render(self.text, True, (0, 0, 0))
        padding = 20
        bubble_w = text_surf.get_width() + padding
        bubble_h = text_surf.get_height() + padding
        bubble_rect = pygame.Rect(0, 0, bubble_w, bubble_h)
        bubble_rect.center = self.pos
        pygame.draw.rect(screen, (255, 255, 255), bubble_rect, border_radius=15)
        pygame.draw.rect(screen, (0, 0, 0), bubble_rect, 2, border_radius=15)
        screen.blit(text_surf, text_surf.get_rect(center=bubble_rect.center))

    def is_expired(self):
        return pygame.time.get_ticks() - self.start_time > self.duration
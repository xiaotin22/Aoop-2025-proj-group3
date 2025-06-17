import pygame

class SpeechBubble:
    def __init__(self, player, pos, font, duration=1500):
        self.text = text
        self.pos = pos  # (x, y) 中心點
        self.font = font
        self.start_time = pygame.time.get_ticks()
        self.duration = duration  # 毫秒
        self.player = player

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
    
    def get_test(self, player):
        if self.player.mood <= self.player.low_mood_limit:
            if self.player.social <= self.player.low_social_limit :
                self.text = "我好像有點不開心..."
                
            elif self.player.knowledge >= self.player.low_knowledge_limit:
                self.text = "我好像有點無聊..."
                
            elif self.player.energy >= self.player.low_energy_limit:
                self.text = "我好像有點累..."
                
            
                
        if self.player.mood >= self.player.high_mood_limit:
            if self.player.social <= self.player.low_social_limit :
                self.text = "我好像有點不開心..."
                
            elif self.player.energy >= self.player.low_energy_limit:
                self.text = "我好像有點累..."
                
            elif self.player.knowledge >= self.player.low_knowledge_limit:
                self.text = "我好像有點無聊..."
                
                
        
        
        
        return self.text
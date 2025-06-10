import pygame

class Button:
    def __init__(self, x, y, width, height, text,  
                 bg_color=(200, 200, 200), 
                 text_color=(0, 0, 0),
                 hover_color=(170, 170, 170),
                 border_radius=12):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = self.font = pygame.font.Font("resource/font/JasonHandwriting3-SemiBold.ttf", 36)
        self.bg_color = bg_color
        self.text_color = text_color
        self.hover_color = hover_color
        self.border_radius = border_radius
        self.is_hovered = False
        self.hover_sound = pygame.mixer.Sound("resource/music/sound_effect/menu_hover.mp3")

    def draw(self, surface):
        # 決定目前顏色
        color = self.hover_color if self.is_hovered else self.bg_color
        pygame.draw.rect(surface, color, self.rect, border_radius=self.border_radius)
        # 畫字
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
    # 偵測滑鼠是否進入按鈕
        mouse_pos = pygame.mouse.get_pos()
        was_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        if self.is_hovered and not was_hovered:
            self.hover_sound.play()  # 只在剛進入時播放

        # 點擊事件
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered:
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
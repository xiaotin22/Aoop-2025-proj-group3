import pygame

class ImageButton:
    def __init__(self, image_path, pos, size=None, text="", font=None, text_color=(50, 50, 50)):
        self.image_original = pygame.image.load(image_path).convert_alpha()
        if size:
            self.image_original = pygame.transform.smoothscale(self.image_original, size)
        self.image = self.image_original

        self.base_pos = pos  # 原始位置
        self.rect = self.image.get_rect(topleft=self.base_pos)

        self.text = text
        self.font = font
        self.text_color = text_color

        self.hover_scale = 1.04
        self.is_hover = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.is_hover = self.rect.collidepoint(mouse_pos)

        if self.is_hover:
            # 放大圖片
            w, h = self.image_original.get_size()
            new_size = (int(w * self.hover_scale), int(h * self.hover_scale))
            self.image = pygame.transform.smoothscale(self.image_original, new_size)

            # 更新位置保持中心不變
            center = (self.base_pos[0] + w // 2, self.base_pos[1] + h // 2)
            self.rect = self.image.get_rect(center=center)
        else:
            # 回復原圖與位置
            self.image = self.image_original
            self.rect = self.image.get_rect(topleft=self.base_pos)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

        if self.text and self.font:
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)

    def is_clicked(self, event):
        return self.rect.collidepoint(event.pos)

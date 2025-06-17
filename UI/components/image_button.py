import pygame

class ImageButton:
    def __init__(self, image_path, pos, size=None, hover_scale=1.05):
        self.image_original = pygame.image.load(image_path).convert_alpha()

        if size:
            self.image_original = pygame.transform.smoothscale(self.image_original, size)

        self.image = self.image_original
        self.rect = self.image.get_rect(topleft=pos)

        self.hover = False
        self.scale = 1.0
        self.hover_scale = hover_scale
        self.center = pos  # 永遠記住原始位置

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        is_hover = self.rect.collidepoint(mouse_pos)

        # 平滑改變縮放比例
        target_scale = self.hover_scale if is_hover else 1.0
        self.scale += (target_scale - self.scale) * 0.2

        # 重新縮放圖片
        w, h = self.image_original.get_size()
        new_size = (int(w * self.scale), int(h * self.scale))
        self.image = pygame.transform.smoothscale(self.image_original, new_size)

        # 設定新 rect 但維持 topleft 不變
        self.rect = self.image.get_rect(topleft=self.center)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pygame.mouse.get_pos())
        return False
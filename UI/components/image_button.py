import pygame

class ImageButton:
    def __init__(self, image_path, pos, size=None, hover_scale=1.05):
        self.image_original = pygame.image.load(image_path).convert_alpha()

        if size:
            self.image_original = pygame.transform.smoothscale(self.image_original, size)

        self.image = self.image_original
        self.center = pos  # ❤️ 改成以 center 為主
        self.hover_scale = hover_scale
        self.scale = 1.0
        self.is_hover = False

        self.update_image()

    def update_image(self):
        w, h = self.image_original.get_size()
        new_w, new_h = int(w * self.scale), int(h * self.scale)
        self.image = pygame.transform.smoothscale(self.image_original, (new_w, new_h))
        self.rect = self.image.get_rect(center=self.center)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        is_now_hover = self.rect.collidepoint(mouse_pos)

        # 平滑縮放
        target_scale = self.hover_scale if is_now_hover else 1.0
        self.scale += (target_scale - self.scale) * 0.2
        self.update_image()

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pygame.mouse.get_pos())
        return False

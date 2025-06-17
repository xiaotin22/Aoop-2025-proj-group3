import pygame

class ImageButton:
    def __init__(self, image_path, pos, scale_hover=1.03, size=None):
        self.image_original = pygame.image.load(image_path).convert_alpha()
        if size:
            self.image_original = pygame.transform.smoothscale(self.image_original, size)
        self.image = self.image_original

        # 用來碰撞的 hitbox，固定大小不變
        self.hitbox = self.image_original.get_rect(topleft=pos)
        self.rect = self.hitbox.copy()  # 實際繪圖用的 rect

        self.hover_scale = scale_hover
        self.is_hover = False

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.hitbox.collidepoint(mouse_pos):  # 偵測用 hitbox
            if not self.is_hover:
                self.is_hover = True
                w, h = self.image_original.get_size()
                self.image = pygame.transform.smoothscale(
                    self.image_original,
                    (int(w * self.hover_scale), int(h * self.hover_scale))
                )
                
                self.rect = self.image.get_rect(center=self.hitbox.center)
        else:
            if self.is_hover:
                self.image = self.image_original
                self.rect = self.hitbox.copy()
                self.is_hover = False

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                return True
        return False


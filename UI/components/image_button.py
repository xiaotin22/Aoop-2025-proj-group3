import pygame

class ImageButton:
    def __init__(self, image_path, pos, scale_hover=1.1):
        self.image_original = pygame.image.load(image_path).convert_alpha()
        self.image = self.image_original
        self.rect = self.image.get_rect(topleft=pos)
        self.hover_scale = scale_hover
        self.is_hover = False

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if not self.is_hover:
                # 滑進來：放大
                self.is_hover = True
                w, h = self.image_original.get_size()
                self.image = pygame.transform.smoothscale(self.image_original, (int(w * self.hover_scale), int(h * self.hover_scale)))
                self.rect = self.image.get_rect(center=self.rect.center)
        else:
            if self.is_hover:
                # 滑走：縮回
                self.image = self.image_original
                self.rect = self.image.get_rect(center=self.rect.center)
                self.is_hover = False

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                return True
        return False


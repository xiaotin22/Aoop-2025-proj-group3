import pygame

class ImageButton:
    def __init__(self, image_path, pos, size=None, text="", font=None, text_color=(0, 0, 0), scale_hover=1.1):
        self.image_original = pygame.image.load(image_path).convert_alpha()
        if size:
            self.image_original = pygame.transform.smoothscale(self.image_original, size)
        self.image = self.image_original
        self.rect = self.image.get_rect(topleft=pos)

        self.hover_scale = scale_hover
        self.is_hover = False

        self.text = text
        self.font = font
        self.text_color = text_color

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if not self.is_hover:
                self.is_hover = True
                w, h = self.image_original.get_size()
                self.image = pygame.transform.smoothscale(
                    self.image_original, (int(w * self.hover_scale), int(h * self.hover_scale))
                )
                self.rect = self.image.get_rect(center=self.rect.center)
        else:
            if self.is_hover:
                self.image = self.image_original
                self.rect = self.image.get_rect(center=self.rect.center)
                self.is_hover = False

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        if self.text and self.font:
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                return True
        return False
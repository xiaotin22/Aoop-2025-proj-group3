import pygame
from UI.components.base_scene import BaseScene
import setting

class DiaryScene(BaseScene):
    def __init__(self, screen):
        super().__init__(screen)

        # diary 圖片
        self.diary = pygame.image.load("resource/image/diary_image.png").convert_alpha()
        self.diary = pygame.transform.smoothscale(self.diary, (800, 600))
        self.diary_rect = self.diary.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))

        # 左右按鈕
        self.left_img = pygame.image.load("resource/image/left.png").convert_alpha()
        self.right_img = pygame.image.load("resource/image/right.png").convert_alpha()
        self.left_img = pygame.transform.smoothscale(self.left_img, (60, 60))
        self.right_img = pygame.transform.smoothscale(self.right_img, (60, 60))

        self.left_rect = self.left_img.get_rect(topleft=(100, 650))
        self.right_rect = self.right_img.get_rect(topleft=(200, 650))
        self.hover_left = False
        self.hover_right = False

    def run(self):
        while self.running:
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.diary, self.diary_rect.topleft)

            mouse_pos = pygame.mouse.get_pos()
            self.hover_left = self.left_rect.collidepoint(mouse_pos)
            self.hover_right = self.right_rect.collidepoint(mouse_pos)

            # 放大效果
            if self.hover_left:
                left_scaled = pygame.transform.smoothscale(self.left_img, (72, 72))
                rect = left_scaled.get_rect(center=self.left_rect.center)
                self.screen.blit(left_scaled, rect.topleft)
            else:
                self.screen.blit(self.left_img, self.left_rect)

            if self.hover_right:
                right_scaled = pygame.transform.smoothscale(self.right_img, (72, 72))
                rect = right_scaled.get_rect(center=self.right_rect.center)
                self.screen.blit(right_scaled, rect.topleft)
            else:
                self.screen.blit(self.right_img, self.right_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    return "BACK"

            pygame.display.flip()
            self.clock.tick(self.FPS)

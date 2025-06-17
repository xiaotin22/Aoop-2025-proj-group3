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

        # 返回按鈕（右上角）
        self.back_img = pygame.image.load("resource/image/back.png").convert_alpha()
        self.back_img = pygame.transform.smoothscale(self.back_img, (60, 60))
        self.back_rect = self.back_img.get_rect(topright=(self.SCREEN_WIDTH - 30, 30))

    def run(self):
        while self.running:
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.diary, self.diary_rect.topleft)

            # 滑鼠位置
            mouse_pos = pygame.mouse.get_pos()

            # 左右按鈕 hover 效果
            self.draw_hover_button(self.left_img, self.left_rect, mouse_pos)
            self.draw_hover_button(self.right_img, self.right_rect, mouse_pos)

            # 返回按鈕 hover 效果
            self.draw_hover_button(self.back_img, self.back_rect, mouse_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.back_rect.collidepoint(event.pos):
                        return "BACK"

            pygame.display.flip()
            self.clock.tick(self.FPS)

    def draw_hover_button(self, img, rect, mouse_pos):
        if rect.collidepoint(mouse_pos):
            scaled = pygame.transform.smoothscale(img, (72, 72))
            new_rect = scaled.get_rect(center=rect.center)
            self.screen.blit(scaled, new_rect.topleft)
        else:
            self.screen.blit(img, rect)

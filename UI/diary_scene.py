import pygame
from UI.components.base_scene import BaseScene
import setting

class DiaryScene(BaseScene):
    def __init__(self, screen):
        super().__init__(screen)

        # 柔和背景顏色
        self.bg_color = (255, 248, 240)  # 淡淡奶油色

        # diary 圖片
        self.diary = pygame.image.load("resource/image/diary_image.png").convert_alpha()
        self.diary = pygame.transform.smoothscale(self.diary, (900, 800))
        self.diary_rect = self.diary.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))

        # 左右按鈕
        self.left_img = pygame.image.load("resource/image/left.png").convert_alpha()
        self.right_img = pygame.image.load("resource/image/right.png").convert_alpha()
        self.left_img = pygame.transform.smoothscale(self.left_img, (80, 80))
        self.right_img = pygame.transform.smoothscale(self.right_img, (80, 80))

        self.left_rect = self.left_img.get_rect(topleft=(470, 600))
        self.right_rect = self.right_img.get_rect(topleft=(630, 600))
        self.hover_left = False
        self.hover_right = False

        # 返回鍵
        self.back_img = pygame.image.load("resource/image/back.png").convert_alpha()
        self.back_img = pygame.transform.smoothscale(self.back_img, (90, 90))
        self.back_rect = self.back_img.get_rect(topleft=(80, 80))
        self.hover_back = False

    def run(self):
        while self.running:
            self.screen.fill(self.bg_color)
            self.screen.blit(self.diary, self.diary_rect.topleft)

            mouse_pos = pygame.mouse.get_pos()
            self.hover_left = self.left_rect.collidepoint(mouse_pos)
            self.hover_right = self.right_rect.collidepoint(mouse_pos)
            self.hover_back = self.back_rect.collidepoint(mouse_pos)

            # 左右按鈕放大
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

            # 返回鍵放大
            if self.hover_back:
                back_scaled = pygame.transform.smoothscale(self.back_img, (72, 72))
                rect = back_scaled.get_rect(center=self.back_rect.center)
                self.screen.blit(back_scaled, rect.topleft)
            else:
                self.screen.blit(self.back_img, self.back_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.back_rect.collidepoint(mouse_pos):
                        return "BACK"
                    if self.left_rect.collidepoint(mouse_pos):
                        print("點擊左鍵")  # 可以換頁
                    if self.right_rect.collidepoint(mouse_pos):
                        print("點擊右鍵")  # 可以換頁

            pygame.display.flip()
            self.clock.tick(self.FPS)

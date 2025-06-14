import pygame
from UI.components.base_scene import BaseScene
from UI.components.image_button import ImageButton

class SetScene(BaseScene):
    def __init__(self, screen):
        super().__init__(screen)

        # 背景圖
        self.bg = pygame.image.load("resource/image/set_page.png").convert_alpha()
        self.bg = pygame.transform.scale(self.bg, screen.get_size())

        # 返回按鈕圖
        self.back_icon = pygame.image.load("resource/image/back.png").convert_alpha()
        self.back_icon = pygame.transform.smoothscale(self.back_icon, (80, 80))
        self.back_rect = self.back_icon.get_rect(topleft=(20, 20))

        # 設定按鈕
        self.button1 = ImageButton("resource/image/button.png", (300, 250))
        self.button2 = ImageButton("resource/image/button.png", (300, 360))

    def run(self):
        while self.running:
            self.screen.blit(self.bg, (0, 0))

            # ✅ hover 放大 back.png
            mouse_pos = pygame.mouse.get_pos()
            if self.back_rect.collidepoint(mouse_pos):
                scaled = pygame.transform.scale(self.back_icon, (96, 96))  # 放大
                rect = scaled.get_rect(center=self.back_rect.center)
                self.screen.blit(scaled, rect.topleft)
            else:
                self.screen.blit(self.back_icon, self.back_rect.topleft)

            # 更新＆畫圖片按鈕
            self.button1.update()
            self.button2.update()
            self.button1.draw(self.screen)
            self.button2.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.back_rect.collidepoint(mouse_pos):
                        return "BACK"

                    if self.button1.is_clicked(event):
                        return "OPTION_1"

                    if self.button2.is_clicked(event):
                        return "OPTION_2"

            pygame.display.flip()
            self.clock.tick(self.FPS)
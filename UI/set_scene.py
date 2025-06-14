import pygame
from UI.components.base_scene import BaseScene
from UI.components.image_button import ImageButton

class SetScene(BaseScene):
    def __init__(self, screen, blurred_bg):
        super().__init__(screen)

        # 模糊背景（由 MainScene 傳入）
        self.blurred_bg = pygame.transform.scale(blurred_bg, screen.get_size())

        # 上層的設定頁面板
        self.panel = pygame.image.load("resource/image/set_page.png").convert_alpha()
        self.panel = pygame.transform.scale(self.panel, screen.get_size())

        # 返回按鈕圖
        self.back_icon = pygame.image.load("resource/image/back.png").convert_alpha()
        self.back_icon = pygame.transform.smoothscale(self.back_icon, (80, 80))
        self.back_rect = self.back_icon.get_rect(topleft=(20, 20))
        self.back_hover = False

        # 設定按鈕（可改位置與大小）
        self.button1 = ImageButton("resource/image/button.png", (360, 170), size=(700, 400))
        self.button2 = ImageButton("resource/image/button.png", (360, 330), size=(700, 400))

    def run(self):
        while self.running:
            self.screen.blit(self.blurred_bg, (0, 0))  # 模糊背景
            self.screen.blit(self.panel, (0, 0))       # 上層面板

            # 🔁 更新 hover 狀態
            mouse_pos = pygame.mouse.get_pos()
            self.back_hover = self.back_rect.collidepoint(mouse_pos)

            # ✅ hover 放大 back.png
            if self.back_hover:
                scaled = pygame.transform.scale(self.back_icon, (96, 96))
                rect = scaled.get_rect(center=self.back_rect.center)
                self.screen.blit(scaled, rect.topleft)
            else:
                self.screen.blit(self.back_icon, self.back_rect.topleft)

            # 更新＆畫圖片按鈕
            self.button1.update()
            self.button2.update()
            self.button1.draw(self.screen)
            self.button2.draw(self.screen)

            # 處理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.back_hover:
                        return "BACK"
                    if self.button1.is_clicked(event):
                        return "OPTION_1"
                    if self.button2.is_clicked(event):
                        return "OPTION_2"

            pygame.display.flip()
            self.clock.tick(self.FPS)

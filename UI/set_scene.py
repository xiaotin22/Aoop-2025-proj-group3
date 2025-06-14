import pygame
from UI.components.base_scene import BaseScene
from UI.components.image_button import ImageButton

class SetScene(BaseScene):
    def __init__(self, screen):
        super().__init__(screen)

        # 背景圖
        self.bg = pygame.image.load("resource/image/set_page.png").convert_alpha()
        self.bg = pygame.transform.scale(self.bg, screen.get_size())

        # 返回圖示
        self.back_icon = pygame.image.load("resource/image/back.png").convert_alpha()
        self.back_icon = pygame.transform.smoothscale(self.back_icon, (80, 80))
        self.back_rect = self.back_icon.get_rect(topleft=(20, 20))

        # 按鈕（可以加更多）
        self.button1 = ImageButton("resource/image/button.png", (260, 160), size=(700, 550))
        self.button2 = ImageButton("resource/image/button.png", (260, 370), size=(700, 550))


    def run(self):
        while self.running:
            self.screen.blit(self.bg, (0, 0))

            # 滑鼠 hover back.png 時放大
            mouse_pos = pygame.mouse.get_pos()
            if self.back_rect.collidepoint(mouse_pos):
                scaled = pygame.transform.scale(self.back_icon, (96, 96))  # 放大
                rect = scaled.get_rect(center=self.back_rect.center)
                self.screen.blit(scaled, rect.topleft)
            else:
                self.screen.blit(self.back_icon, self.back_rect.topleft)

            # 更新 & 畫出按鈕
            self.button1.update()
            self.button2.update()
            self.button1.draw(self.screen)
            self.button2.draw(self.screen)

            # 事件處理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.back_rect.collidepoint(pygame.mouse.get_pos()):
                        print("🟢 偵測到返回點擊")
                        return "BACK"
                    if self.button1.is_clicked(event):
                        return "OPTION_1"
                    if self.button2.is_clicked(event):
                        return "OPTION_2"

            pygame.display.flip()
            self.clock.tick(self.FPS)

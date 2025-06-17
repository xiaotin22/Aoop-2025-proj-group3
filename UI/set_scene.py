import pygame
from UI.components.base_scene import BaseScene
from UI.components.image_button import ImageButton

class SetScene(BaseScene):
    def __init__(self, screen, blurred_bg, week_number):
        super().__init__(screen)
        self.week_number = week_number

        self.blurred_bg = pygame.transform.scale(blurred_bg, screen.get_size())

        self.panel = pygame.image.load("resource/image/set_page.png").convert_alpha()
        self.panel = pygame.transform.scale(self.panel, screen.get_size())

        self.back_icon = pygame.image.load("resource/image/back.png").convert_alpha()
        self.back_icon = pygame.transform.smoothscale(self.back_icon, (80, 80))
        self.back_rect = self.back_icon.get_rect(topleft=(200, 157))
        self.back_hover = False

        # 👇 兩個 hover 放大圖片按鈕
        self.button1 = ImageButton("resource/image/button.png", (290, 95), size=(600, 450))
        self.button2 = ImageButton("resource/image/button.png", (290, 260), size=(600, 450))

        # 字體（週數）
        self.week_font = pygame.font.Font("resource/font/ChenYuluoyan-Thin-Monospaced.ttf", 42)

    def draw_week_number(self):
        text = f"第 {self.week_number} 週"
        surface = self.week_font.render(text, True, (255, 245, 200))  # 淺黃色
        shadow = self.week_font.render(text, True, (100, 80, 60))
        x = self.SCREEN_WIDTH // 2 - surface.get_width() // 2
        y = 175
        self.screen.blit(shadow, (x + 2, y + 2))
        self.screen.blit(surface, (x, y))

    def run(self):
        while self.running:
            self.screen.blit(self.blurred_bg, (0, 0))
            self.screen.blit(self.panel, (0, 0))
            self.draw_week_number()

            # hover 放大返回鍵
            mouse_pos = pygame.mouse.get_pos()
            self.back_hover = self.back_rect.collidepoint(mouse_pos)
            if self.back_hover:
                scaled = pygame.transform.scale(self.back_icon, (96, 96))
                rect = scaled.get_rect(center=self.back_rect.center)
                self.screen.blit(scaled, rect.topleft)
            else:
                self.screen.blit(self.back_icon, self.back_rect.topleft)

            # 更新＆繪製按鈕
            self.button1.update()
            self.button2.update()
            self.button1.draw(self.screen)
            self.button2.draw(self.screen)

            # 事件處理
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
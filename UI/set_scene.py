import pygame
from UI.components.base_scene import BaseScene
from UI.components.image_button import ImageButton
import setting

class SetScene(BaseScene):
    def __init__(self, screen, blurred_bg, week_number):
        super().__init__(screen)
        self.week_number = week_number

        self.blurred_bg = pygame.transform.scale(blurred_bg, screen.get_size())


        # ✅ 上層的設定頁面板
        self.panel = pygame.image.load(setting.ImagePath.SET_PAGE_PATH).convert_alpha()
        self.panel = pygame.transform.scale(self.panel, screen.get_size())

        # ✅ 返回按鈕圖
        self.back_icon = pygame.image.load(setting.ImagePath.BACK_PATH).convert_alpha()

        self.back_icon = pygame.transform.smoothscale(self.back_icon, (80, 80))
        self.back_rect = self.back_icon.get_rect(topleft=(200, 157))  # 你原本的位置
        self.back_hover = False

        # 顯示第幾週
        self.week_number = week_number
        self.week_font = pygame.font.Font("resource/font/ChenYuluoyan-Thin-Monospaced.ttf", 48)

        
        # ✅ 設定按鈕（可自由調整位置與大小）
        self.button1 = ImageButton(setting.ImagePath.BUTTON_PATH, (260, 70), size=(650, 550))
        self.button2 = ImageButton(setting.ImagePath.BUTTON_PATH, (260, 280), size=(650, 550))

    def draw_week_number(self):
        font = pygame.font.Font("resource/font/ChenYuluoyan-Thin-Monospaced.ttf", 42)
        text = f"第 {self.week_number} 週"

        text_surface = font.render(text, True, (255, 245, 200))
        shadow_surface = font.render(text, True, (100, 80, 60))
        x = self.SCREEN_WIDTH // 2 - text_surface.get_width() // 2
        y = 175
        self.screen.blit(shadow_surface, (x + 2, y + 2))   # 陰影微偏右下
        self.screen.blit(text_surface, (x, y))


    def run(self):
        while self.running:
            self.screen.blit(self.blurred_bg, (0, 0))  # 模糊背景
            self.screen.blit(self.panel, (0, 0))       # 上層面板
            self.draw_week_number()

            # hover 狀態更新
            mouse_pos = pygame.mouse.get_pos()
            self.back_hover = self.back_rect.collidepoint(mouse_pos)

            # 返回鍵放大
            if self.back_hover:
                scaled = pygame.transform.scale(self.back_icon, (96, 96))
                rect = scaled.get_rect(center=self.back_rect.center)
                self.screen.blit(scaled, rect.topleft)
            else:
                self.screen.blit(self.back_icon, self.back_rect.topleft)

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
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
        self.button1 = ImageButton("resource/image/button.png", (600, 355), size=(600, 450))
        self.button2 = ImageButton("resource/image/button.png", (600, 515), size=(600, 450))

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

            from UI.components.image_button import ImageButton  # 如果還沒加

            self.yes_button = ImageButton("resource/image/button.png", (400, 350), size=(300, 150), text="是", font_path="resource/font/ChenYuluoyan-Thin-Monospaced.ttf", font_size=42)
            self.no_button = ImageButton("resource/image/button.png", (800, 350), size=(300, 150), text="否", font_path="resource/font/ChenYuluoyan-Thin-Monospaced.ttf", font_size=42)

            # 更新＆畫圖片按鈕
            self.button1.update()
            self.button2.update()
            self.button1.draw(self.screen)
            self.button2.draw(self.screen)

            # --- 第一顆按鈕：音量調整 ---
            base_font_size = 50
            scaled_size1 = int(base_font_size * self.button1.scale)
            font1 = pygame.font.Font("resource/font/ChenYuluoyan-Thin-Monospaced.ttf", scaled_size1)
            text1 = font1.render("音量調整", True, (50, 50, 50))
            text_rect1 = text1.get_rect(center=self.button1.rect.center)
            self.screen.blit(text1, text_rect1)

            # --- 第二顆按鈕：重新開始 ---
            scaled_size2 = int(base_font_size * self.button2.scale)
            font2 = pygame.font.Font("resource/font/ChenYuluoyan-Thin-Monospaced.ttf", scaled_size2)
            text2 = font2.render("重新開始", True, (50, 50, 50))
            text_rect2 = text2.get_rect(center=self.button2.rect.center)
            self.screen.blit(text2, text_rect2)

            # 事件處理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.back_hover:
                        return "BACK"
                    if self.button1.is_clicked(event):
                        from UI.sound_control_scene import SoundControlScene
                        sound_scene = SoundControlScene(self.screen)
                        sound_scene.run()
                        # 回來之後繼續待在設定頁
                        continue
                    elif self.button2.is_clicked(event):
                        from UI.confirm_reborn_scene import ConfirmRebornScene
                        confirm_scene = ConfirmRebornScene(self.screen)
                        confirm_result = confirm_scene.run()
                        if confirm_result == "REBORN":
                            return "GO_TO_START"
                        elif confirm_result == "BACK":
                            continue  # 留在設定頁

            pygame.display.flip()
            self.clock.tick(self.FPS)
import pygame
from UI.components.base_scene import BaseScene
from UI.components.image_button import ImageButton
import setting

class DiaryScene(BaseScene):
    def __init__(self, screen, player):
        super().__init__(screen)
        self.player = player

        self.diary_img = pygame.image.load("resource/image/diary_image.png").convert_alpha()
        self.diary_img = pygame.transform.smoothscale(self.diary_img, (1200, 1100))
        self.diary_rect = self.diary_img.get_rect(center=(610, 450))

        self.font = pygame.font.Font("resource/font/ChenYuluoyan-Thin-Monospaced.ttf",38)
        print("是否載入字體成功？", self.font)

        self.week_index = 0
        self.total_weeks = len(self.player.event_history)

        self.btn_left = ImageButton("resource/image/left.png", (100, 700), size=(80, 80))
        self.btn_right = ImageButton("resource/image/right.png", (980, 700), size=(80, 80))
        self.btn_back = ImageButton("resource/image/back.png", (90, 20), size=(100, 100))

    def wrap_text(self, text, font, max_width):
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
        return lines

    def draw_multiline_text(self, surface, text, pos, font=None, color=(50, 30, 30), max_width=600, line_height=40):
        if font is None:
            font = self.font
        x, y = pos
        lines = self.wrap_text(text, font, max_width)
        for line in lines:
            txt_surf = font.render(line, True, color)
            surface.blit(txt_surf, (x, y))
            y += line_height

    def draw(self):
        self.screen.fill((245, 240, 225))  # 柔和米白色
        self.screen.blit(self.diary_img, self.diary_rect)

        if self.player.event_history:
            print(self.player.event_history)
            print("正在讀取第", self.week_index, "週日記")
            sorted_weeks = sorted(self.player.event_history.keys())
            if self.week_index < len(sorted_weeks):
                week = sorted_weeks[self.week_index]
                entry = self.player.event_history.get(week)
                event_text = entry.get("event_text", "")
                option_text = entry.get("option_text", "")
                changes = entry.get("changes", {})

                self.draw_multiline_text(self.screen, f"📒 第 {week} 週回顧", (200, 210), line_height=50)
                self.draw_multiline_text(self.screen, f"事件內容：\n{event_text}", (200, 290))
                self.draw_multiline_text(self.screen, f"你的選擇：\n{option_text}", (200, 430))

                change_text = "狀態變化：\n"
                for attr, value in changes.items():
                    if value != 0:
                        change_text += f"{attr} +{value} \n"
                self.draw_multiline_text(self.screen, change_text, (200, 490))

        self.btn_left.draw(self.screen)
        self.btn_right.draw(self.screen)
        self.btn_back.draw(self.screen)

    def run(self):
        while self.running:
            self.btn_left.update()
            self.btn_right.update()
            self.btn_back.update()
            
            self.draw()
            pygame.display.flip()
            self.clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.btn_left.rect.collidepoint(event.pos):
                        self.week_index = max(0, self.week_index - 1)
                    elif self.btn_right.rect.collidepoint(event.pos):
                        self.week_index = min(self.total_weeks - 1, self.week_index + 1)
                    elif self.btn_back.rect.collidepoint(event.pos):
                        return "BACK"
        return None
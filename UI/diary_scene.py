import pygame
from UI.components.base_scene import BaseScene
import setting

class DiaryScene(BaseScene):
    def __init__(self, screen, player):
        super().__init__(screen)
        self.player = player
        self.current_week_index = 0

        # 背景色（柔和米色）
        self.bg_color = (255, 248, 230)

        # Diary 圖片
        self.diary = pygame.image.load("resource/image/diary_image.png").convert_alpha()
        self.diary = pygame.transform.smoothscale(self.diary, (800, 600))
        self.diary_rect = self.diary.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))

        # 左右按鈕
        self.left_img = pygame.image.load("resource/image/left_btn.png").convert_alpha()
        self.right_img = pygame.image.load("resource/image/right_btn.png").convert_alpha()
        self.left_img = pygame.transform.smoothscale(self.left_img, (60, 60))
        self.right_img = pygame.transform.smoothscale(self.right_img, (60, 60))
        self.left_rect = self.left_img.get_rect(topleft=(100, 650))
        self.right_rect = self.right_img.get_rect(topleft=(200, 650))

        # 返回按鈕
        self.back_img = pygame.image.load("resource/image/back.png").convert_alpha()
        self.back_img = pygame.transform.smoothscale(self.back_img, (60, 60))
        self.back_rect = self.back_img.get_rect(topleft=(30, 30))

        # 狀態
        self.hover_left = False
        self.hover_right = False
        self.hover_back = False

        # 字型
        self.title_font = pygame.font.Font(setting.JFONT_PATH_BOLD, 48)
        self.text_font = pygame.font.Font(setting.JFONT_PATH_REGULAR, 28)

    def draw_text(self, surface, text, pos, font, color=(50, 30, 10), max_width=700):
        words = text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        lines.append(current_line.strip())
        x, y = pos
        for line in lines:
            rendered = font.render(line, True, color)
            surface.blit(rendered, (x, y))
            y += font.get_linesize() + 5

    def run(self):
        while self.running:
            self.screen.fill(self.bg_color)
            self.screen.blit(self.diary, self.diary_rect)

            mouse_pos = pygame.mouse.get_pos()
            self.hover_left = self.left_rect.collidepoint(mouse_pos)
            self.hover_right = self.right_rect.collidepoint(mouse_pos)
            self.hover_back = self.back_rect.collidepoint(mouse_pos)

            # 畫按鈕（有 hover 放大）
            self.screen.blit(
                pygame.transform.smoothscale(self.left_img, (72, 72)) if self.hover_left else self.left_img,
                self.left_rect)
            self.screen.blit(
                pygame.transform.smoothscale(self.right_img, (72, 72)) if self.hover_right else self.right_img,
                self.right_rect)
            self.screen.blit(
                pygame.transform.smoothscale(self.back_img, (72, 72)) if self.hover_back else self.back_img,
                self.back_rect)

            if 0 <= self.current_week_index < len(self.player.event_history):
                entry = self.player.event_history[self.current_week_index]
                week_title = f"第 {entry['week']} 週"
                self.draw_text(self.screen, week_title, (150, 100), self.title_font)

                self.draw_text(self.screen, "事件：", (150, 170), self.text_font)
                self.draw_text(self.screen, entry["event_text"], (180, 210), self.text_font)

                self.draw_text(self.screen, "你的選擇：", (150, 310), self.text_font)
                self.draw_text(self.screen, entry["option_text"], (180, 350), self.text_font)

                self.draw_text(self.screen, "影響：", (150, 450), self.text_font)
                stat_map = {"study": "知識", "social": "社交", "play_game": "娛樂", "rest": "休息"}
                change_lines = [f"{stat_map[k]} +{v}" for k, v in entry["changes"].items() if v != 0]
                self.draw_text(self.screen, "，".join(change_lines), (180, 490), self.text_font)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.hover_back:
                        return "BACK"
                    elif self.hover_left and self.current_week_index > 0:
                        self.current_week_index -= 1
                    elif self.hover_right and self.current_week_index < len(self.player.event_history) - 1:
                        self.current_week_index += 1

            pygame.display.flip()
            self.clock.tick(self.FPS)

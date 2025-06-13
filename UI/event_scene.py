import pygame
import sys
import json
from components.base_scene import BaseScene, wrap_text


class EventScene(BaseScene ):
    def __init__(self, screen, player):
        super().__init__(screen)
        
        self.player = player
        # 背景圖片
        self.background_img = pygame.image.load("resource/image/background_intro.png").convert()

        # 便條紙圖片
        note_img = pygame.image.load("resource/image/event_window.PNG").convert_alpha()
        orig_width, orig_height = note_img.get_size()

        # 假設想讓寬度變成 800，等比例縮放高度
        target_width = 800
        scale_factor = target_width / orig_width
        target_height = int(orig_height * scale_factor)

        self.note_img = pygame.transform.smoothscale(note_img, (target_width, target_height))
        self.note_rect = self.note_img.get_rect(center=(600, 400))

        self.font = pygame.font.Font("resource/font/JasonHandwriting3-SemiBold.ttf", 36)
        self.font_small = pygame.font.Font("resource/font/JasonHandwriting3-Regular.ttf", 32)

        # 載入所有週資料
        with open("event/events.json", "r", encoding="utf-8") as f:
            self.all_weeks_data = json.load(f)

        # 預設顯示第 2 週
        self.current_week = f"week_{self.player.week_number}"  # 假設玩家從第1週開始，這裡顯示第2週
        self.week_data = self.all_weeks_data[self.current_week]

        # 事件文字（取第一個事件的描述）
        self.event_text = self.week_data["events"][0]["description"]

        # 選項轉成 [(text, key), ...]
        self.options = []
        for key, option in self.week_data["events"][0]["options"].items():
            self.options.append((option["text"], key))

        # 按鈕設定
        self.BUTTON_COLOR = (200, 180, 150)
        self.BUTTON_HOVER_COLOR = (255, 220, 180)
        self.BUTTON_TEXT_COLOR = (50, 30, 10)
        self.button_width = 520
        self.button_height = 60
        self.button_margin = 15
        self.max_text_width = self.button_width - 20

        # 按鈕位置計算
        start_x = self.note_rect.centerx - 260
        start_y = self.note_rect.centery - 30  # 便條紙底部往上留空間放按鈕

        self.buttons = []
        for i, (text, key) in enumerate(self.options):
            rect = pygame.Rect(
                start_x,
                start_y + i * (self.button_height + self.button_margin),
                self.button_width,
                self.button_height
            )
            self.buttons.append((rect, text, key))

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for rect, text, key in self.buttons:
                    if rect.collidepoint(pos):
                        print(f"你選擇了選項 {key}: {text}")
                        
    def draw(self):
        self.screen.blit(self.background_img, (0, 0))  # 畫背景
        self.screen.blit(self.note_img, self.note_rect)  # 畫便條紙

        # 畫事件文字（多行換行）
        max_event_width = self.note_img.get_width() - 250
        event_lines = wrap_text(self.event_text, self.font, max_event_width)
        for i, line in enumerate(event_lines):
            line_surf = self.font.render(line, True, (50, 50, 50))
            # 文字位置依照便條紙中心調整
            self.screen.blit(line_surf, (self.note_rect.centerx - 230, self.note_rect.centery - 200 + i * (self.font.get_height() + 5)))

        for rect, text, key in self.buttons:
            # 半透明按鈕背景帶圓角
            button_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            alpha = 180  # 透明度
            color = self.BUTTON_HOVER_COLOR if rect.collidepoint(pygame.mouse.get_pos()) else self.BUTTON_COLOR
            rgba_color = (*color, alpha)
            pygame.draw.rect(button_surf, rgba_color, button_surf.get_rect(), border_radius=8)
            self.screen.blit(button_surf, (rect.left, rect.top))

            # 文字換行成兩行，並垂直置中
            lines = wrap_text(key + ". " + text, self.font_small, self.max_text_width)
            line_height = self.font_small.get_height()
            total_text_height = line_height * len(lines)
            start_text_y = rect.top + (rect.height - total_text_height) // 2

            for idx, line in enumerate(lines):
                text_surf = self.font_small.render(line, True, self.BUTTON_TEXT_COLOR)
                text_rect = text_surf.get_rect()
                text_rect.left = rect.left + 10
                text_rect.top = start_text_y + idx * line_height
                self.screen.blit(text_surf, text_rect)


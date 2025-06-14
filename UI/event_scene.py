import pygame
import sys
import json
from UI.components.base_scene import BaseScene, wrap_text
from UI.components.button import Button


class EventScene(BaseScene ):
    def __init__(self, screen, player):
        super().__init__(screen)
        self.player = player
        self.background_img = pygame.image.load("resource/image/background_intro.png").convert()
        note_img = pygame.image.load("resource/image/event_window.PNG").convert_alpha()
        orig_width, orig_height = note_img.get_size()
        target_width = 850
        scale_factor = target_width / orig_width
        target_height = int(orig_height * scale_factor)
        self.note_img = pygame.transform.smoothscale(note_img, (target_width, target_height))
        self.note_rect = self.note_img.get_rect(center=(600, 400))

        self.font = pygame.font.Font("resource/font/JasonHandwriting3-SemiBold.ttf", 36)
        self.font_small = pygame.font.Font("resource/font/JasonHandwriting3-Regular.ttf", 28)

        with open("event/events.json", "r", encoding="utf-8") as f:
            self.all_weeks_data = json.load(f)
        self.week_data = self.all_weeks_data[f"week_{self.player.week_number}"]

        if len(self.week_data["events"]) != 0:
            self.event_text = self.week_data["events"]["description"]
        else:
            return "finished"

        self.options = []
        for key, option in self.week_data["events"]["options"].items():
            self.options.append((option["text"], key))

        self.BUTTON_COLOR = (200, 180, 150)
        self.BUTTON_HOVER_COLOR = (255, 220, 180)
        self.BUTTON_TEXT_COLOR = (50, 30, 10)
        self.button_width = 545
        self.button_height = 70
        self.button_margin = 20
        self.max_text_width = self.button_width - 20

        # 動畫屬性
        self.note_anim_x = -1000  # 從螢幕左外側開始
        self.note_target_x = self.note_rect.x
        self.animating_in = True

        # 計算按鈕初始位置
        self.buttons = []
        for i, (text, key) in enumerate(self.options):
            button_y = self.note_rect.centery - 30 + i * (self.button_height + self.button_margin)
            button = (Button(self.note_rect.centerx - 260, button_y,
                             self.button_width, self.button_height, key + "." + text, self.font_small,
                             self.BUTTON_COLOR, self.BUTTON_TEXT_COLOR, self.BUTTON_HOVER_COLOR), key)
            self.buttons.append(button)

    def update(self):
        if self.animating_in:
            # 緩動滑入
            speed = 40
            if self.note_anim_x < self.note_target_x:
                self.note_anim_x += speed
                if self.note_anim_x >= self.note_target_x:
                    self.note_anim_x = self.note_target_x
                    self.animating_in = False
            return  # 動畫時不處理事件

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            for button in self.buttons:
                if button[0].handle_event(event):
                    attribute = self.week_data["events"]["options"][button[1]]["attribute"]
                    if "study" in attribute:
                        self.player.study()
                    if "social" in attribute:
                        self.player.socialize()
                    if "play_game" in attribute:
                        self.player.play_game()
                    if "rest" in attribute:
                        self.player.rest()
                    self.player.chosen[self.player.week_number] = button[1]
                    print(f"你選擇了選項 {button[1]}: {button[0].text}")
                    return "finished"

    def draw(self):
        self.screen.blit(self.background_img, (0, 0))
        # 便條紙滑入
        note_rect_anim = self.note_rect.copy()
        note_rect_anim.x = int(self.note_anim_x)
        self.screen.blit(self.note_img, note_rect_anim)

        # 文字滑入
        lines = self.event_text.splitlines() if self.event_text else []
        # 文字根據 note_rect_anim.x 偏移
        text_offset_x = note_rect_anim.x - self.note_rect.x
        self.draw_lines(self.screen, lines, self.font, start_pos=(388 + text_offset_x, 200))

        # 按鈕滑入
        for i, button in enumerate(self.buttons):
            btn = button[0]
            btn_x = btn.rect.x + text_offset_x
            btn_y = btn.rect.y
            btn.rect.topleft = (btn_x, btn_y)
            btn.draw(self.screen)
            # 恢復原本 x，避免 hover 判斷錯誤
            btn.rect.topleft = (btn_x - text_offset_x, btn_y)

    def draw_lines(self, surface, lines, font, start_pos=(388, 200), color=(0, 0, 0)):
        x, y = start_pos
        line_spacing = 10
        line_height = font.get_linesize()
        for line in lines:
            txt_surf = font.render(line, True, color)
            surface.blit(txt_surf, (x, y))
            y += line_height + line_spacing



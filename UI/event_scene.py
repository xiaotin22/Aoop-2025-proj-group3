import pygame
import sys
import json
from UI.components.base_scene import BaseScene, wrap_text
from UI.components.button import Button


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
        target_width = 850
        scale_factor = target_width / orig_width
        target_height = int(orig_height * scale_factor)

        self.note_img = pygame.transform.smoothscale(note_img, (target_width, target_height))
        self.note_rect = self.note_img.get_rect(center=(600, 400))

        self.font = pygame.font.Font("resource/font/JasonHandwriting3-SemiBold.ttf", 36)
        self.font_small = pygame.font.Font("resource/font/JasonHandwriting3-Regular.ttf", 28)

        # 載入所有週資料
        with open("event/events.json", "r", encoding="utf-8") as f:
            self.all_weeks_data = json.load(f)

        self.week_data = self.all_weeks_data[f"week_{self.player.week_number}"]

        # 事件文字（取第一個事件的描述）
        if len(self.week_data["events"]) != 0:
            self.event_text = self.week_data["events"]["description"]
            
        else :
            return "finished"

        # 選項轉成 [(text, key), ...]
        self.options = []
        for key, option in self.week_data["events"]["options"].items():
            self.options.append((option["text"], key))

        # 按鈕設定
        self.BUTTON_COLOR = (200, 180, 150)
        self.BUTTON_HOVER_COLOR = (255, 220, 180)
        self.BUTTON_TEXT_COLOR = (50, 30, 10)
        self.button_width = 545
        self.button_height = 70
        self.button_margin = 20
        self.max_text_width = self.button_width - 20

        # 按鈕位置計算
        start_x = self.note_rect.centerx - 260
        start_y = self.note_rect.centery - 30  # 便條紙底部往上留空間放按鈕

        self.buttons = []
        for i, (text, key) in enumerate(self.options):
            button = ( Button(start_x, 
                   start_y + i * (self.button_height + self.button_margin),
                   self.button_width, self.button_height, key +"." + text, self.font_small, 
                   self.BUTTON_COLOR, self.BUTTON_TEXT_COLOR,
                   self.BUTTON_HOVER_COLOR), key)
            self.buttons.append(button)

    def update(self):
        self.paste_in_note(final_center=self.note_rect.center)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            for button in self.buttons :
                if button[0].handle_event(event):
                    attribute =  self.week_data["events"]["options"][button[1]]["attribute"]
                    if "study" in attribute :
                        self.player.study()
                        
                    if "social" in attribute :
                        self.player.socialize()
                    
                    if "play_game" in attribute :
                        self.player.play_game()
                    
                    if "rest" in attribute :
                        self.player.rest()
                        
                    self.player.chosen[self.player.week_number] = button[1]
                    print(f"你選擇了選項 {button[1]}: {button[0].text}")
                    return "finished"
                        
    def draw(self):
        self.screen.blit(self.background_img, (0, 0))  # 畫背景
     
        
        lines = self.event_text.splitlines() if self.event_text else []
        self.draw_lines(self.screen, lines, self.font)

        for button in self.buttons:
            button[0].draw(self.screen)
            
    def draw_lines(self, surface, lines, font, start_pos=(388, 200), color=(0, 0, 0)):
        x, y = start_pos
        line_spacing = 10
        line_height = font.get_linesize()

        for line in lines:
            txt_surf = font.render(line, True, color)
            surface.blit(txt_surf, (x, y))
            y += line_height + line_spacing
            
def _draw_scaled_note(self, scale, center):
    self.screen.blit(self.background_img, (0, 0))
    
    # 縮放 note
    new_size = (int(self.note_img.get_width() * scale), int(self.note_img.get_height() * scale))
    scaled_note = pygame.transform.smoothscale(self.note_img, new_size)
    note_rect = scaled_note.get_rect(center=center)

    # 畫文字在背景上（可以移除）
    self.draw_lines(self.screen, self.event_text.splitlines(), self.font)

    # 畫 note
    self.screen.blit(scaled_note, note_rect)

    pygame.display.update()

def paste_in_note(self, final_center=(600, 400), steps=15):
    """
    模擬便條紙從小到大貼上螢幕的動畫，附帶彈一下的縮放效果
    """
    clock = pygame.time.Clock()

    # 初始縮放比例
    start_scale = 0.2
    overshoot_scale = 1.1  # 貼上時稍微放大一點
    final_scale = 1.0

    for i in range(steps):
        progress = i / steps
        scale = start_scale + (overshoot_scale - start_scale) * progress
        self._draw_scaled_note(scale, final_center)
        clock.tick(60)

    # 彈回正常大小
    for i in range(steps // 2):
        progress = i / (steps // 2)
        scale = overshoot_scale - (overshoot_scale - final_scale) * progress
        self._draw_scaled_note(scale, final_center)
        clock.tick(60)




            


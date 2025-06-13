import pygame
import json
import sys

# -------- EventScene --------
class EventScene:
    def __init__(self, screen, events):
        self.screen = screen
        self.events = events
        self.font = pygame.font.Font("/home/chen/oop-2025-proj-group10/resource/font/JasonHandwriting3-Regular.ttf", 28)
        self.current_event_index = 0
        self.running = True

    def draw(self):
        self.screen.fill((240, 240, 240))

        if self.current_event_index < len(self.events):
            event = self.events[self.current_event_index]
            desc = event["description"]
            options = event["options"]

            # 事件描述
            y = 50
            for line in desc.split('\n'):
                desc_text = self.font.render(line, True, (0, 0, 0))
                self.screen.blit(desc_text, (50, y))
                y += 30

            # 選項
            y += 20
            for key, opt in options.items():
                opt_text = self.font.render(f"{key}. {opt['text']}", True, (0, 0, 0))
                self.screen.blit(opt_text, (70, y))
                y += 30

            # 指示文字
            info_text = self.font.render("點擊畫面繼續下一事件", True, (80, 80, 80))
            self.screen.blit(info_text, (50, y + 20))

        else:
            end_text = self.font.render("事件結束，點擊返回主畫面", True, (0, 0, 0))
            self.screen.blit(end_text, (50, 50))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.current_event_index < len(self.events):
                self.current_event_index += 1
            else:
                self.running = False

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.handle_event(event)

            self.draw()
            pygame.display.flip()
            clock.tick(30)
        return True  # 事件完成


# -------- MainScene --------
class MainScene:
    def __init__(self, screen):
        self.screen = screen
        # 讀取JSON事件資料
        with open('event/events.json', 'r', encoding='utf-8') as f:
            self.story_dict = json.load(f)

        self.current_week = 1
        self.font = pygame.font.Font("/home/chen/oop-2025-proj-group10/resource/font/JasonHandwriting3-Regular.ttf", 28)

        # 紀錄事件是否完成
        self.event_finished = {f"week_{i}": False for i in range(1, 17)}

        # 按鈕區域設定
        self.next_week_rect = pygame.Rect(1000, 700, 150, 50)
        self.event_button_rect = pygame.Rect(800, 700, 150, 50)

    def has_event_this_week(self):
        week_key = f"week_{self.current_week}"
        events = self.story_dict.get(week_key, {}).get("events", [])
        events = story_dict.get("week_1", {}).get("events", [])

        for event in events:
            description = event.get("description", " ")
            print(description)

        return len(events) > 0 and not self.event_finished[week_key]

    def draw(self):
        self.screen.fill((180, 200, 230))

        # 顯示週次
        week_title = self.story_dict.get(f"week_{self.current_week}", {}).get("title", "")
        text = self.font.render(f"第 {self.current_week} 週 - {week_title}", True, (0, 0, 0))
        self.screen.blit(text, (50, 50))

        # 下一週按鈕
        pygame.draw.rect(self.screen, (100, 180, 100), self.next_week_rect)
        next_text = self.font.render("下一週", True, (255, 255, 255))
        text_rect = next_text.get_rect(center=self.next_week_rect.center)
        self.screen.blit(next_text, text_rect)

        # 事件按鈕（有事件且未完成時亮起）
        if self.has_event_this_week():
            pygame.draw.rect(self.screen, (255, 215, 0), self.event_button_rect)  # 黃色
            event_text = self.font.render("有事件！點我", True, (0, 0, 0))
        else:
            pygame.draw.rect(self.screen, (150, 150, 150), self.event_button_rect)  # 灰色
            event_text = self.font.render("無事件", True, (100, 100, 100))
        text_rect = event_text.get_rect(center=self.event_button_rect.center)
        self.screen.blit(event_text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            if self.next_week_rect.collidepoint(pos):
                if self.current_week < 16:
                    self.current_week += 1
            elif self.event_button_rect.collidepoint(pos) and self.has_event_this_week():
                self.open_event_scene()

        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def open_event_scene(self):
        week_key = f"week_{self.current_week}"
        events = self.story_dict.get(week_key, {}).get("events", [])
        event_scene = EventScene(self.screen, events)
        finished = event_scene.run()
        if finished:
            self.event_finished[week_key] = True

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                self.handle_event(event)

            self.draw()
            pygame.display.flip()
            clock.tick(30)


# -------- 主程式 --------
def main():
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("大學生模擬遊戲")

    main_scene = MainScene(screen)
    main_scene.run()

if __name__ == "__main__":
    main()

import pygame
from UI.components.base_scene import BaseScene
from UI.components.image_button import ImageButton
import setting

class DiaryScene(BaseScene):
    def __init__(self, screen, player):
        super().__init__(screen)
        self.player = player
        self.current_week = 1
        self.total_weeks = len(player.event_history)

        self.bg_color = (255, 248, 240)
        self.font = pygame.font.Font(setting.JFONT_PATH_REGULAR, 28)
        self.font_bold = pygame.font.Font(setting.JFONT_PATH_BOLD, 32)

        self.diary_img = pygame.image.load("resource/image/diary/diary_image.png")
        self.diary_img = pygame.transform.smoothscale(self.diary_img, (900, 600))
        self.diary_rect = self.diary_img.get_rect(center=(600, 400))

        self.left_btn = ImageButton("resource/image/diary/left.png", (250, 670), scale=1.0)
        self.right_btn = ImageButton("resource/image/diary/right.png", (950, 670), scale=1.0)
        self.back_btn = ImageButton("resource/image/button/back.png", (30, 30), scale=1.0)

    def draw_text(self, text, pos, max_width=700, color=(0, 0, 0)):
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            if self.font.size(test_line)[0] > max_width:
                lines.append(current_line)
                current_line = word + " "
            else:
                current_line = test_line
        lines.append(current_line)

        x, y = pos
        for line in lines:
            surface = self.font.render(line.strip(), True, color)
            self.screen.blit(surface, (x, y))
            y += self.font.get_linesize() + 4

    def draw(self):
        self.screen.fill(self.bg_color)
        self.screen.blit(self.diary_img, self.diary_rect)

        if self.current_week in self.player.event_history:
            entry = self.player.event_history[self.current_week]
            title = f"第 {self.current_week} 週"
            event = entry["event_text"]
            option = entry["option_text"]
            changes = entry["changes"]

            self.screen.blit(self.font_bold.render(title, True, (90, 50, 20)), (330, 180))
            self.draw_text("事件：" + event, (330, 240))
            self.draw_text("你的選擇：" + option, (330, 320))

            change_text = f"狀態變化：心情 {format_change(changes['mood'])}、體力 {format_change(changes['energy'])}、社交 {format_change(changes['social'])}、知識 {format_change(changes['knowledge'])}"
            self.draw_text(change_text, (330, 410))

        self.left_btn.draw(self.screen)
        self.right_btn.draw(self.screen)
        self.back_btn.draw(self.screen)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.left_btn.handle_event(event):
                if self.current_week > 1:
                    self.current_week -= 1
            if self.right_btn.handle_event(event):
                if self.current_week < self.total_weeks:
                    self.current_week += 1
            if self.back_btn.handle_event(event):
                return "BACK"

    def run(self):
        while self.running:
            result = self.update()
            if result is not None:
                return result
            self.draw()
            pygame.display.flip()
            self.clock.tick(self.FPS)
        return None

def format_change(value):
    return f"+{value}" if value > 0 else str(value)

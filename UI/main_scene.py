import pygame
import os
import json
from UI.components.character_animator import CharacterAnimator
from UI.components.button import Button
from UI.components.audio_manager import AudioManager
from UI.components.base_scene import BaseScene


class MainScene(BaseScene):
    def __init__(self, screen, player):
        super().__init__(screen)
        self.background = pygame.image.load("resource/image/background_intro.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, self.screen.get_size())
        self.animator = CharacterAnimator(player.intro, (400, 400),(300, 300))
        font = pygame.font.Font("resource/font/JasonHandwriting3-SemiBold.ttf", 36)
        self.next_week_button = Button(
            self.SCREEN_WIDTH - 200, self.SCREEN_HEIGHT - 100,
            180, 60,"下一週", font, (200, 200, 250),(50, 50, 50) ,(180, 180, 180))

        excl_img = pygame.image.load("resource/image/event_icon.PNG").convert_alpha()
        self.excl_img = pygame.transform.smoothscale(excl_img, (175, 175))
        self.excl_rect = self.excl_img.get_rect(center=(430, 400))
        self.excl_mask = pygame.mask.from_surface(self.excl_img)
        self.player = player
        self.is_hover = False      # 是否目前 hover 狀態
        self.hover_scale = 1.1
        if player.name == "Bubu":
            self.animator.frame_delay = 10  # 控制動畫速度

        self.stats_font = pygame.font.Font("resource/font/JasonHandwriting3-Regular.ttf", 28)
        self.bar_width = 150
        self.bar_height = 20
        self.bar_gap = 10
        self.bar_colors = {
            "intelligence": (135, 206, 250),  # 淺藍
            "mood":         (255, 182, 193),  # 粉紅
            "energy":       (144, 238, 144),  # 淺綠
            "social":       (255, 165, 0),    # 橘色
            "knowledge":    (160, 32, 240)    # 紫色
        }


    def update(self):
        self.animator.update()
       

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        relative_pos = (mouse_pos[0] - self.excl_rect.left, mouse_pos[1] - self.excl_rect.top)

        # 判斷是否在圖片形狀內 hover
        if (0 <= relative_pos[0] < self.excl_rect.width and
            0 <= relative_pos[1] < self.excl_rect.height and
            self.excl_mask.get_at(relative_pos)):
            if not self.is_hover:
                # 剛 hover
                self.audio.play_sound("resource/music/sound_effect/menu_hover.mp3")
                self.is_hover = True

            if mouse_pressed[0]:
                if self.player.chosen[self.player.week_number] == '0' :
                    return "Open Event"
                else :
                    print("this week's event has been done !")
        else:
            self.is_hover = False


    def draw_player_stats(self):

        stats_bg = pygame.Surface((480, 250), pygame.SRCALPHA)
        stats_bg.fill((255, 255, 255, 180))  # 180 可調整透明度，0~255

        # 貼到主畫面
        self.screen.blit(stats_bg, (20, 50))

        # 畫邊框
        pygame.draw.rect(self.screen, (100, 100, 100), (20, 50, 480, 250), 2)

        stats = {
            "intelligence": self.player.intelligence,
            "mood": self.player.mood,
            "energy": self.player.energy,
            "social": self.player.social,
            "knowledge": self.player.knowledge
        }

        font = self.stats_font
        x_left = 30
        x_right = x_left + self.bar_width + 80
        y_start = 180
        bar_height = self.bar_height
        bar_width = self.bar_width
        gap_y = self.bar_gap
        label_offset = -5  # 調整文字與條的對齊

        # 第一排：intelligence / mood
        for i, key in enumerate(["intelligence", "mood"]):
            x = x_left if i == 0 else x_right
            y = y_start
            fill = max(0, min(1, stats[key] / 100))
            pygame.draw.rect(self.screen, (200, 200, 200), (x + 65, y, bar_width, bar_height), 2)
            pygame.draw.rect(self.screen, self.bar_colors[key], (x + 65, y, int(bar_width * fill), bar_height))
            label = font.render(f"智力 {self.player.intelligence}" if key == "intelligence" else f"心情 {self.player.mood}", True, (0, 0, 0))
            self.screen.blit(label, (x, y + label_offset))

        # 第二排：energy / social
        for i, key in enumerate(["energy", "social"]):
            x = x_left if i == 0 else x_right
            y = y_start + bar_height + gap_y +10
            fill = max(0, min(1, stats[key] / 100))
            pygame.draw.rect(self.screen, (200, 200, 200), (x + 65, y, bar_width, bar_height), 2)
            pygame.draw.rect(self.screen, self.bar_colors[key], (x + 65, y, int(bar_width * fill), bar_height))
            label = font.render(f"體力 {self.player.energy}" if key == "energy" else f"社交 {self.player.social}", True, (0, 0, 0))
            self.screen.blit(label, (x, y + label_offset))
        
        # 第三排：knowledge（橫跨兩個 bar）
        y = y_start + 2 * (bar_height + gap_y) + 20
        x = x_left
        total_width = (x_right - x_left) + 130 + bar_width  # 橫跨兩欄
        fill = max(0, min(1, stats["knowledge"] / 100))
        pygame.draw.rect(self.screen, (200, 200, 200), (x + 65, y, total_width - 130, bar_height), 2)
        pygame.draw.rect(self.screen, self.bar_colors["knowledge"], (x + 130, y, int((total_width - 130) * fill), bar_height))
        label = font.render(f"知識 {self.player.knowledge:.0f}/100", True, (0, 0, 0))
        self.screen.blit(label, (x, y + label_offset))
        

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.animator.draw(self.screen)
        self.next_week_button.draw(self.screen)
        self.draw_player_stats()

        if self.player.chosen[self.player.week_number] == '0':
            # ====== 閃爍動畫（基礎 scale）======
            ticks = pygame.time.get_ticks()
            import math
            base_scale = 1 + 0.12 * math.sin(ticks * 0.01)  # 在 0.95 到 1.05 之間震盪

            # ====== hover 放大疊加效果 ======
            if self.is_hover:
                scale = base_scale * self.hover_scale
            else:
                scale = base_scale

            # ====== 計算縮放後的位置並繪製 ======
            new_width = int(self.excl_img.get_width() * scale)
            new_height = int(self.excl_img.get_height() * scale)
            scaled_img = pygame.transform.smoothscale(self.excl_img, (new_width, new_height))
            scaled_rect = scaled_img.get_rect(center=self.excl_rect.center)
            
            self.screen.blit(scaled_img, scaled_rect)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "Quit"
                if self.next_week_button.handle_event(event):
                    return "Next Story"
            if self.update()!= None :
                return self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(self.FPS)
        return None


 
   
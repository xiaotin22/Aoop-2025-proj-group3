import pygame
from UI.components.base_scene import BaseScene
from UI.main_scene import MainScene
from UI.components.character_animator import CharacterAnimator
from UI.components.audio_manager import AudioManager

class EndScene(MainScene):
    def __init__(self, screen, player):
        super().__init__(screen, player)
        self.background = pygame.image.load(
            "resource/image/background_intro.png"
        ).convert_alpha()
        self.background = pygame.transform.scale(
            self.background, self.screen.get_size()
        )
        self.background.set_alpha(100)
        
        self.player = player
        self.title_font = pygame.font.Font(
            "resource/font/JasonHandwriting3-SemiBold.ttf", 54
        )
        self.subtitle_font = pygame.font.Font(
            "resource/font/JasonHandwriting3-Regular.ttf", 48
        )

        # ---------- 音樂 ----------    
        self.audio = AudioManager.get_instance()
        self.audio.play_bgm("resource/music/bgm/yier_bubu.MP3")


        # ---------- 按鈕 ----------
        self.buttons = []
        button_texts = [
            ("重新開始", "RESTART"),
            ("顯示排行", "SHOW_RANK"),
            ("回饋表單", "FEEDBACK"),
            ("退出遊戲", "QUIT"),
        ]
        button_w, button_h, spacing = 300, 70, 30
        total_h = len(button_texts) * (button_h + spacing) - spacing
        start_y = (self.SCREEN_HEIGHT - total_h) // 2 + 100

        for i, (text, action) in enumerate(button_texts):
            rect = pygame.Rect(
                (self.SCREEN_WIDTH - button_w) // 2 + 250,
                start_y + i * (button_h + spacing),
                button_w,
                button_h,
            )
            self.buttons.append(
                {
                    "rect": rect,
                    "text": text,
                    "action": action,
                    "hover": False,
                    "hovered_last": False,
                    "scale": 1.0,
                }
            )

        # ---------- 裝飾動畫 ----------
        self.animator2 = CharacterAnimator(self.player.ending, (50, 400), (300, 300))
        
        self.animator2.frame_delay = 3
        # ---------- 其他 ----------
        self.selected_result = None

    # -------------------------------------------------------------
    # 更新邏輯 & 事件處理
    # -------------------------------------------------------------
    def update(self):
        self.clock.tick(self.FPS)
        
        self.animator2.update()
        mouse_pos = pygame.mouse.get_pos()

        # 事件處理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for btn in self.buttons:
                    if btn["rect"].collidepoint(mouse_pos):
                        return btn["action"]

        # 按鈕 hover 更新
        for btn in self.buttons:
            is_hovered = btn["rect"].collidepoint(mouse_pos)
            if is_hovered and not btn["hovered_last"]:
                self.audio.play_sound("resource/music/sound_effect/bo.MP3")
            btn["hovered_last"] = is_hovered
            btn["hover"] = is_hovered

            target_scale = 1.1 if is_hovered else 1.0
            btn["scale"] += (target_scale - btn["scale"]) * 0.2

        # 無需切換場景時回傳 None
        return None

    # -------------------------------------------------------------
    # 畫面渲染
    # -------------------------------------------------------------
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

        # 印出玩家的頭像
        player_imaage = pygame.image.load(self.player.header).convert_alpha()
        player_image = pygame.transform.smoothscale(player_imaage, (100, 100))
        player_rect = player_image.get_rect(topleft=(40, 60))
        self.screen.blit(player_image, player_rect)
        # 印出玩家的名字
        name_label = font.render(self.player.chname + " " + self.player.name, True, (0, 0, 0))
        name_rect = name_label.get_rect(topleft=(160, 80))
        self.screen.blit(name_label, name_rect)
        # 印出玩家的週數
        week_label = font.render("Final Result", True, (0, 0, 0))
        week_rect = week_label.get_rect(topleft=(160, 120))
        self.screen.blit(week_label, week_rect)

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
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.background, (0, 0))
        self.draw_player_stats()
        # 裝飾動畫
        self.animator2.draw(self.screen)

        # 標題
        title_surf = self.title_font.render(
            f"Congratulation!!", True, (50, 50, 50)
        )
        title_rect = title_surf.get_rect(center=(self.SCREEN_WIDTH // 2 + 200, 150))
        self.screen.blit(title_surf, title_rect)

        # 印出玩家的GPA
        gpa_surf = self.subtitle_font.render(
            f"{self.player.name}'s Final GPA：{self.player.GPA:.2f}", True, (50, 50, 50)
        )
        gpa_rect = gpa_surf.get_rect(center=(self.SCREEN_WIDTH // 2 + 200, 200))
        self.screen.blit(gpa_surf, gpa_rect)

        # 副標題
        subtitle_surf = self.subtitle_font.render(
            f"期中考：{self.player.midterm}, 期末考：{self.player.final}", True, (50, 50, 50)
        )
        subtitle_rect = subtitle_surf.get_rect(center=(self.SCREEN_WIDTH // 2 + 200 , 250))
        self.screen.blit(subtitle_surf, subtitle_rect)


        # 按鈕
        for btn in self.buttons:
            rect = btn["rect"]
            scaled_rect = pygame.Rect(
                0,
                0,
                int(rect.width * btn["scale"]),
                int(rect.height * btn["scale"]),
            )
            scaled_rect.center = rect.center

            base_color = (200, 200, 250) if btn["hover"] else (180, 180, 180)
            border_color = (120, 120, 160)
            pygame.draw.rect(self.screen, base_color, scaled_rect, border_radius=15)
            pygame.draw.rect(self.screen, border_color, scaled_rect, 3, border_radius=15)

            text_surf = self.subtitle_font.render(btn["text"], True, (50, 50, 50))
            text_rect = text_surf.get_rect(center=scaled_rect.center)
            self.screen.blit(text_surf, text_rect)

        pygame.display.flip()

    # -------------------------------------------------------------
    # 主循環
    # -------------------------------------------------------------
    def run(self):
        while self.running:
            result = self.update()
            if result is not None:
                return result
            self.draw()



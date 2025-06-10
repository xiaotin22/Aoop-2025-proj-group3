import pygame
import os
from UI.scene_manager import Scene

    
class StartScene(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        self.background = pygame.image.load("resource/image/background_intro.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, self.screen.get_size())
        self.background.set_alpha(100)

        self.title_font = pygame.font.Font("resource/font/JasonHandwriting3-SemiBold.ttf", 72)
        self.subtitle_font = pygame.font.Font("resource/font/JasonHandwriting3-Regular.ttf", 48)
        self.selected_result = None

        # 背景音樂
        pygame.mixer.music.load('resource/music/bgm/yier_bubu.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        # 建立按鈕
        self.buttons = []
        button_texts = [("開始遊戲", "START"), ("顯示介紹", "SHOW_INTRO"), ("排行榜", "RANK"), ("退出遊戲", "QUIT")]
        button_width = 300
        button_height = 70
        spacing = 30
        total_height = len(button_texts) * (button_height + spacing) - spacing
        start_y = (self.SCREEN_HEIGHT - total_height) // 2 + 50

        for i, (text, action) in enumerate(button_texts):
            rect = pygame.Rect(
                (self.SCREEN_WIDTH - button_width) // 2,
                start_y + i * (button_height + spacing),
                button_width,
                button_height
            )
            self.buttons.append({
                "rect": rect,
                "text": text,
                "action": action,
                "hover": False,
                "hovered_last": False,
                "scale": 1.0
            })

        # 🎀 裝飾動畫：載入 + 個別縮放 + 記錄 index
        self.decorations = [
            [pygame.transform.smoothscale(f, (220, 220)) for f in self.load_frames("resource/gif/four_char_frames")],
            [pygame.transform.smoothscale(f, (220, 220)) for f in self.load_frames("resource/gif/four_char2_frames")]
        ]
        self.decoration_positions = [
            (50, 500),     # 左下角
            (900, 150),    # 右上角
        ]
        
        self.decoration_indices = [0] * len(self.decorations)  # 每組目前播放到哪一幀
        self.decoration_anim_counters = [0] * len(self.decorations)  # 每組動畫幀等待計數
        self.decoration_anim_delay = 5  # 🎈每幾幀換一張圖（數字越大越慢）

    def run(self):
        while self.running:
            self.clock.tick(self.FPS)
            mouse_pos = pygame.mouse.get_pos()
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))

            # 處理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for btn in self.buttons:
                        if btn["rect"].collidepoint(mouse_pos):
                            self.selected_result = btn["action"]
                            return self.selected_result

            # 🎀 播放裝飾動畫# 🎀 播放裝飾動畫（平滑版本）
            for i, (frames, pos) in enumerate(zip(self.decorations, self.decoration_positions)):
                # 幀等待累積器
                self.decoration_anim_counters[i] += 1
                if self.decoration_anim_counters[i] >= self.decoration_anim_delay:
                    self.decoration_anim_counters[i] = 0
                    self.decoration_indices[i] = (self.decoration_indices[i] + 1) % len(frames)

                frame = frames[self.decoration_indices[i]]
                self.screen.blit(frame, pos)

            # 標題
            title_surface = self.title_font.render("Welcome to Our Game!", True, (50, 50, 50))
            title_rect = title_surface.get_rect(center=(self.SCREEN_WIDTH // 2, 150))
            self.screen.blit(title_surface, title_rect)

            # 按鈕們
            for btn in self.buttons:
                rect = btn["rect"]
                is_hovered = rect.collidepoint(mouse_pos)
                # 音效
                if is_hovered and not btn["hovered_last"]:
                    self.hover_sound.play()
                btn["hovered_last"] = is_hovered
                btn["hover"] = is_hovered

                # 縮放按鈕
                target_scale = 1.1 if is_hovered else 1.0
                btn["scale"] += (target_scale - btn["scale"]) * 0.2

                # 縮放按鈕矩形
                scaled_width = int(rect.width * btn["scale"])
                scaled_height = int(rect.height * btn["scale"])
                scaled_rect = pygame.Rect(0, 0, scaled_width, scaled_height)
                scaled_rect.center = rect.center

                # 畫按鈕背景
                base_color = (200, 200, 250) if is_hovered else (180, 180, 180)
                border_color = (120, 120, 160)
                pygame.draw.rect(self.screen, base_color, scaled_rect, border_radius=15)
                pygame.draw.rect(self.screen, border_color, scaled_rect, 3, border_radius=15)

                # 畫按鈕文字
                text_surface = self.subtitle_font.render(btn["text"], True, (50, 50, 50))
                text_rect = text_surface.get_rect(center=scaled_rect.center)
                self.screen.blit(text_surface, text_rect)

            pygame.display.flip()

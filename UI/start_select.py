import pygame
import os

class Scene:
    def __init__(self, screen):
        self.screen = screen
        self.SCREEN_HEIGHT = 800
        self.SCREEN_WIDTH = 1200
        self.clock = pygame.time.Clock()
        self.FPS = 30
        self.running = True
        self.font = pygame.font.Font("resource/font/JasonHandwriting3-SemiBold.ttf", 36)
        self.font_desc = pygame.font.Font("resource/font/JasonHandwriting3-Regular.ttf", 28)
        self.hover_sound = pygame.mixer.Sound("resource/music/sound_effect/menu_hover.mp3")
        self.char_size = (140, 140)

        # 背景圖片
        self.background = pygame.image.load("resource/image/background_intro.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, self.screen.get_size())
        self.background.set_alpha(100)
    
    def load_frames(self, folder_path):
        frames = []
        for filename in sorted(os.listdir(folder_path)):
            if filename.endswith(".png"):
                img = pygame.image.load(os.path.join(folder_path, filename)).convert_alpha()
                img = pygame.transform.scale(img, self.char_size)
                frames.append(img)
        return frames
    
    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return lines    
    
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


class CharacterSelectScene(Scene):
    def __init__(self, screen):
        super().__init__(screen)

        self.frame_index = 0
        self.hovered_character = None
        self.char_size = (140, 140)
        self.box_width, self.box_height = 500, 300
        self.margin = 30
        self.selected_character = None
        # 播放背景音樂
        pygame.mixer.music.load('resource/music/bgm/Mitao_Huihui.mp3')
        pygame.mixer.music.set_volume(0.5)  # 設定音量
        pygame.mixer.music.play(-1)

        # 載入角色圖片
        self.characters = [
            {
                "name": "布布 Bubu",
                "frames": self.load_frames("resource/gif/bubu_intro_frames"),
                "description": "大家好～我是布布！ 我喜歡在網路上盡情地打遊戲！ \n 希望這學期所有的課都可以過 \n 教授...菜菜...撈撈...",
                "box": pygame.Rect(self.margin, self.margin, self.box_width, self.box_height),
                "color": (255, 200, 200),         # 常態紅棕色
                "hover_color": (200, 100, 100)    # Hover 粉紅紅
            },
            {
                "name": "一二 Yier",
                "description": "大家好～我是一二！ 我熱衷於系上活動以及社團～ \n 認識好多學長姐嘿嘿～ 到處吃瓜聽八卦真爽！",
                "frames": self.load_frames("resource/gif/yier_intro_frames"),
                "box": pygame.Rect(self.SCREEN_WIDTH - self.margin - self.box_width, self.margin, self.box_width, self.box_height),
                "color": (150, 200, 255),         # 常態藍色
                "hover_color": (100, 150, 200)    # Hover 淺藍
            },
            {
                "name": "蜜桃 Mitao",
                "description": "大家好～我是蜜桃！ 嗚嗚嗚這學期不小心選太多課... \n 現在實在是捲不動了～ \n 但我還是會努力拿卷的！",
                "frames": self.load_frames("resource/gif/mitao_intro_frames"),
                "box": pygame.Rect(self.margin, self.SCREEN_HEIGHT - self.margin - self.box_height, self.box_width, self.box_height),
                "color": (255, 200, 200),         # 桃色
                "hover_color": (255, 120, 180)    # 淺桃
            },
            {
                "name": "灰灰 Huihui",
                "description": "大家好～我是灰灰！\n 我正在追求自己真正想做的事! \n 讀書不是重點 ! \n 重要的是追尋我的快樂貓生！",
                "frames": self.load_frames("resource/gif/huihui_intro_frames"),
                "box": pygame.Rect(self.SCREEN_WIDTH - self.margin - self.box_width, self.SCREEN_HEIGHT - self.margin - self.box_height, self.box_width, self.box_height),
                "color": (200, 200, 200),            # 常態黑灰
                "hover_color": (80, 80, 80)    # Hover 灰白
            },
        ]

    def run(self):
        while self.running:
            self.clock.tick(self.FPS)
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for char in self.characters:
                        if char["box"].collidepoint(mouse_pos):
                            self.selected_character = char["name"]
                            self.running = False  # 跳出選角場景
            
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))
            

            if pygame.time.get_ticks() % (1000 // self.FPS * 5) < (1000 // self.FPS):
                self.frame_index = (self.frame_index + 1) % len(self.characters[0]["frames"])

            for char in self.characters:
                rect = char["box"]
                is_hovered = rect.collidepoint(mouse_pos)

                # 畫角色框
                overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                overlay.fill((255, 255, 255, 220))  # 白色 + 透明度
                self.screen.blit(overlay, (rect.left, rect.top))

                # 邊框
                border_color = char["hover_color"] if is_hovered else char["color"]
                pygame.draw.rect(self.screen, border_color, rect, 5)


                # 音效
                if is_hovered and self.hovered_character != char["name"]:
                    self.hover_sound.play()
                    self.hovered_character = char["name"]
                elif not is_hovered and self.hovered_character == char["name"]:
                    self.hovered_character = None

                # 圖片（右下對齊）
                frame = char["frames"][self.frame_index]
                img_x = rect.right - frame.get_width() - 20
                img_y = rect.bottom - frame.get_height() - 20
                self.screen.blit(frame, (img_x, img_y))

                # 名字（左下角）
                name_surface = self.font.render(char["name"], True, (50, 50, 50))
                self.screen.blit(name_surface, (rect.left + 20, rect.bottom - 50))

                # 描述（左上角）
                desc_lines = self.wrap_text(char["description"], self.font_desc, rect.width - 100)
                for i, line in enumerate(desc_lines):
                    line_surface = self.font_desc.render(line, True, (100, 100, 100))
                    self.screen.blit(line_surface, (rect.left + 20, rect.top + 20 + i * 40))

            pygame.display.flip()
        return self.selected_character
    
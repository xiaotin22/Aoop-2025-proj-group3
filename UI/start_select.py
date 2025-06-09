import pygame
import os

class CharacterSelectScene:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.FPS = 30
        self.frame_index = 0
        self.hovered_character = None
        self.running = True

        self.char_size = (140, 140)
        self.box_width, self.box_height = 500, 300
        self.margin = 30
        self.font = pygame.font.Font("resource/font/JasonHandwriting3-Light.ttf", 36)
        self.hover_sound = pygame.mixer.Sound("resource/music/sound_effect/menu_hover.mp3")
        self.selected_character = None
        # 播放背景音樂
        pygame.mixer.music.load('resource/music/bgm/Mitao_Huihui.mp3')
        pygame.mixer.music.play(-1)

        # 載入背景圖片
        self.background = pygame.image.load("resource/image/background_intro.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, self.screen.get_size())
        self.background.set_alpha(100)

        # 載入角色圖片
        self.characters = [
            {
                "name": "布布 Bubu",
                "frames": self.load_frames("resource/gif/bubu_intro_frames"),
                "box": pygame.Rect(self.margin, self.margin, self.box_width, self.box_height),
                "color": (255, 200, 200),         # 常態紅棕色
                "hover_color": (200, 100, 100)    # Hover 粉紅紅
            },
            {
                "name": "一二 Yier",
                "frames": self.load_frames("resource/gif/yier_intro_frames"),
                "box": pygame.Rect(1200 - self.margin - self.box_width, self.margin, self.box_width, self.box_height),
                "color": (150, 200, 255),         # 常態藍色
                "hover_color": (100, 150, 200)    # Hover 淺藍
            },
            {
                "name": "蜜桃 Mitao",
                "frames": self.load_frames("resource/gif/mitao_intro_frames"),
                "box": pygame.Rect(self.margin, 800 - self.margin - self.box_height, self.box_width, self.box_height),
                "color": (255, 200, 200),         # 桃色
                "hover_color": (255, 120, 180)    # 淺桃
            },
            {
                "name": "灰灰 Huihui",
                "frames": self.load_frames("resource/gif/huihui_intro_frames"),
                "box": pygame.Rect(1200 - self.margin - self.box_width, 800 - self.margin - self.box_height, self.box_width, self.box_height),
                "color": (200, 200, 200),            # 常態黑灰
                "hover_color": (80, 80, 80)    # Hover 灰白
            },
        ]


    def load_frames(self, folder_path):
        frames = []
        for filename in sorted(os.listdir(folder_path)):
            if filename.endswith(".png"):
                img = pygame.image.load(os.path.join(folder_path, filename)).convert_alpha()
                img = pygame.transform.scale(img, self.char_size)
                frames.append(img)
        return frames

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

                # 圖片（右對齊）
                frame = char["frames"][self.frame_index]
                img_x = rect.right - frame.get_width() - 20
                img_y = rect.top + 20
                self.screen.blit(frame, (img_x, img_y))

                # 名字（左下角）
                name_surface = self.font.render(char["name"], True, (50, 50, 50))
                self.screen.blit(name_surface, (rect.left + 20, rect.bottom - 50))

            pygame.display.flip()
        return self.selected_character
    
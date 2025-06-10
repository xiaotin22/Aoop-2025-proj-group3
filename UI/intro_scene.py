import pygame
from UI.scene_manager import Scene 

class IntroScene(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        self.overlay_surface = pygame.Surface(screen.get_size()).convert_alpha()
        self.overlay_alpha = 0

        self.full_text = (
            "歡迎來到模擬人生大學版\n"
            "在這裡，你的每一週都充滿未知挑戰與選擇\n"
            "你會選擇耍廢？還是成為人生勝利組？\n"
            "遊戲中的每一步選擇都將影響你的角色發展\n"
            "在這個遊戲中，你將有四個角色可以選!\n"
            "從課業到社交，從挑戰到成就，每一週都是新的冒險\n"
            "按下Enter並點選開始遊戲選擇跟你最像的角色吧!\n"
        )
        self.display_text = ""
        self.char_index = 0
        self.type_speed = 2
        self.text_lines = []
        self.frame_count = 0

        self.type_sound = pygame.mixer.Sound("resource/music/sound_effect/typing.mp3")
        self.has_played_sound = False

         # === ✅ 載入GIF影格 ===
        self.gif_frames = self.load_frames("resource/gif/yier_play_game_frames")
        self.gif_index = 0
        self.gif_timer = 0  # 幾個frame換一次圖
        self.gif_delay = 2
        


    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                self.handle_event(event)

            self.update()
            self.draw(self.screen)
            pygame.display.update()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and self.char_index >= len(self.full_text):
                self.running = False

    
    def update(self):
        self.frame_count += 1
        if self.overlay_alpha < 200:
            self.overlay_alpha += 4

        if self.char_index < len(self.full_text) and self.frame_count % self.type_speed == 0:
            self.display_text += self.full_text[self.char_index]
            self.char_index += 1

            self.text_lines = self.wrap_text(self.display_text, self.font, self.SCREEN_WIDTH - 200)

            # ✅ 只播放一次音效
            if not self.has_played_sound:
                self.type_sound.play()
                self.has_played_sound = True

            # ✅ 更新GIF影格
            self.gif_timer += 1
            if self.gif_timer >= self.gif_delay:
                self.gif_index = (self.gif_index + 1) % len(self.gif_frames)
                self.gif_timer = 0



    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        # 黑幕
        self.overlay_surface.fill((0, 0, 0, self.overlay_alpha))
        screen.blit(self.overlay_surface, (0, 0))

        # 顯示分行文字
        y = 150
        for line in self.text_lines:
            rendered = self.font.render(line, True, (255, 255, 255))
            screen.blit(rendered, (100, y))
            y += 75

        # 顯示提示文字
        if self.char_index >= len(self.full_text):
            hint = self.font.render("按 Enter 返回", True, (200, 200, 200))
            screen.blit(hint, (self.SCREEN_WIDTH - 300, self.SCREEN_HEIGHT - 60))

         # ✅ 顯示GIF在右上角
        if self.gif_frames:
            frame = self.gif_frames[self.gif_index]
            frame_rect = frame.get_rect(topright=(self.SCREEN_WIDTH - 50, 50))
            screen.blit(frame, frame_rect)

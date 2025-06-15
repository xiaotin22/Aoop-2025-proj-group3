import pygame
import math
import random
from UI.components.base_scene import BaseScene


class LuckyWheelScene(BaseScene):
    def __init__(self, screen):
        super().__init__(screen)
        self.center = (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2)
        self.angle = 90
        self.spin_speed = 0
        self.wheel_radius = 300
        self.is_spinning = False
        self.font = pygame.font.Font("resource/font/JasonHandwriting3-Regular.ttf", 48)
        self.font_desc = pygame.font.Font("resource/font/JasonHandwriting3-Regular.ttf", 28)
        self.background = pygame.image.load("resource/image/background_intro.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, self.screen.get_size())
        self.background.set_alpha(100)
        self.button_radius = 80
        self.result_text = None
        self.options = [
            "帥潮學長\n超可愛學姐",
            "有點宅宅的學長\n看起來是系邊",
            "的超搞笑系核\n就表演倒立走路\n第一次見面",
            "卷哥卷姐",
            "被放生了"
        ]

        # 新增：載入輪盤圖片
        self.wheel_img = pygame.image.load("resource/image/luckywheel/5.png").convert_alpha()
        self.wheel_img = pygame.transform.smoothscale(self.wheel_img, (self.wheel_radius*2.5, self.wheel_radius*2.5))

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            dx = event.pos[0] - self.center[0]
            dy = event.pos[1] - self.center[1]
            if dx * dx + dy * dy <= self.button_radius * self.button_radius and not self.is_spinning:
                self.audio.play_sound("resource/music/sound_effect/menu_hover.MP3")
                self.start_spin()
                
        

    def start_spin(self):
        self.is_spinning = True
        self.spin_speed = random.uniform(25, 30)
        self.target_angle = None
        self.result_text = None
        self.audio.play_sound("resource/music/sound_effect/luckywheel.mp3")

    def update(self):
        if self.is_spinning:
            self.angle += self.spin_speed
            
            self.spin_speed *= 0.98
            if self.spin_speed < 0.5:
                self.spin_speed = 0
                self.is_spinning = False
                self.calculate_result()


    def calculate_result(self):
        n = len(self.options)
        degrees_per_segment = 360 / n
        segment_angle =  [(i * degrees_per_segment) for i in range(n)]
        index = min(range(n), key=lambda i: abs((self.angle % 360) - segment_angle[i]))
        self.result_text = self.options[index]

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.background, (0, 0))


        # 畫輪盤圖片（旋轉）
        rotated_img = pygame.transform.rotozoom(self.wheel_img, self.angle, 1)
        rect = rotated_img.get_rect(center=self.center)
        self.screen.blit(rotated_img, rect)

        # 畫選項文字
        n = len(self.options)
        degrees_per_segment = 360 / 5
        for i in range(n):
            mid_angle = math.radians(self.angle + (i + 0.5) * degrees_per_segment)
            lines = self.options[i].splitlines() if self.options[i] else []
            for j, line in enumerate(lines):
                # 從外往內排
                r = self.wheel_radius * 0.6 - j * 32  # 32為行距，可調整
                tx = self.center[0] + r * math.cos(mid_angle)
                ty = self.center[1] + r * math.sin(mid_angle)
                text_surface = self.font_desc.render(line, True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=(tx, ty))
                self.screen.blit(text_surface, text_rect)
        


        # Draw center button as circle
        pygame.draw.circle(self.screen, (250, 100, 100), self.center, self.button_radius)
        button_text = self.font.render("抽獎", True, (255, 255, 255))
        text_rect = button_text.get_rect(center=self.center)
        self.screen.blit(button_text, text_rect)

        # Draw blinking pointer (triangle)
        pointer_alpha = 255  # 固定不閃爍
        pointer_surface = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
        pointer = [
            (self.center[0], self.center[1] - self.button_radius  - 30),
            (self.center[0] - 15, self.center[1] - self.button_radius +10),
            (self.center[0] + 15, self.center[1] - self.button_radius +10)
        ]
        pygame.draw.polygon(pointer_surface, (250, 100, 100, pointer_alpha), pointer)
        self.screen.blit(pointer_surface, (0, 0))

        if self.result_text:
            tip = self.font.render("（點擊以結束）", True, (150, 150, 150))
            self.screen.blit(tip, (self.screen.get_width() // 2 - tip.get_width() // 2, 730))
            result_lines = ["抽中"] + self.result_text.splitlines()
            base_x = 950
            base_y = 600
            for j, line in enumerate(result_lines):
                result_surface = self.font_desc.render(line, True, (0, 0, 0))
                result_rect = result_surface.get_rect(center=(base_x, base_y + j * 32))
                self.screen.blit(result_surface, result_rect)
        
       
    
    def run(self):
        self.running = True
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                else:
                    self.handle_event(event)
                    
                if self.result_text and (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN):
                    self.running = False
            self.update()
            self.draw()
            pygame.display.flip()
            clock.tick(self.FPS)
          
            
        return self.result_text
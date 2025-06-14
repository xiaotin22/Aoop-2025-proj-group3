import pygame
import sys
import json
from UI.components.base_scene import BaseScene
from UI.components.audio_manager import AudioManager

class StoryScene(BaseScene):
    def __init__(self, screen, current_week):
        super().__init__(screen)
        
        self.current_week = current_week

        # 讀取故事
        with open('event/events.json', 'r', encoding='utf-8') as f:
            story_dict = json.load(f)

        self.title_font = pygame.font.Font("resource/font/JasonHandwriting3-SemiBold.ttf", 48)
        self.font = pygame.font.Font("resource/font/JasonHandwriting3-Regular.ttf", 36)
        

        self.background = pygame.image.load(f"resource/image/backgrounds/week_1.png")
        self.background = pygame.image.load(f"resource/image/backgrounds/week_1.png")
        self.background = pygame.transform.scale(self.background, screen.get_size())
        self.background.set_alpha(65)


        self.char_interval = 120  # 字母出現間隔（毫秒）
        self.line_spacing = 10
        self.line_height = self.font.get_linesize()

        intro_text = story_dict.get(f"week_{current_week}", {}).get("intro", "")
        self.lines = intro_text.splitlines() if intro_text else []
        self.title = story_dict.get(f"week_{current_week}", {}).get("title", "")

        self.current_line = 0
        self.current_char = 0
        self.displayed_lines = []
        self.last_char_time = pygame.time.get_ticks()
        self.all_finished = False
        self.running = True

        # 開始打字音效
        self.audio.play_sound("resource/music/sound_effect/typing.mp3")  # 迴圈播放

                

  

    def update(self):
        print(pygame.mouse.get_pos())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.all_finished:
                    self.running = False  # 點擊結束故事
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if not self.all_finished:
                        # 把剩下的文字一次顯示出來
                        while self.current_line < len(self.lines):
                            self.displayed_lines.append(self.lines[self.current_line])
                            self.current_line += 1
                        self.all_finished = True
                        self.audio.stop_sound("resource/music/sound_effect/typing.mp3")

                    
            
                    
        now = pygame.time.get_ticks()

        if not self.all_finished and now - self.last_char_time > self.char_interval:
            self.last_char_time = now
            self.current_char += 1
            if self.current_char > len(self.lines[self.current_line]):
                self.displayed_lines.append(self.lines[self.current_line])
                self.current_line += 1
                self.current_char = 0
                if self.current_line >= len(self.lines):
                    self.all_finished = True
                    self.audio.stop_sound("resource/music/sound_effect/typing.mp3")


    def draw(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.background, (0, 0))


        # 假設左右邊距 40，上方起始高度 160
        left_margin = 100
        top_start = 230

        # 畫標題
        if self.title:
            title_surface = self.title_font.render(self.title, True, (50, 50, 50))
            title_rect = title_surface.get_rect()
            title_rect.topleft = (left_margin-30, 120)
            self.screen.blit(title_surface, title_rect)
        # 畫標題與內文的分隔線
        pygame.draw.line(self.screen, (100, 100, 100), (left_margin-50, 180), (self.screen.get_width() - left_margin, 180), 2)
       
        # 已顯示的完整行
        y = top_start
        for line in self.displayed_lines:
            text_surface = self.font.render(line, True, (50, 50, 50))
            self.screen.blit(text_surface, (left_margin, y))
            y += self.line_height + self.line_spacing

        # 當前行正在打字的部分
        if not self.all_finished and self.current_line < len(self.lines):
            partial_text = self.lines[self.current_line][:self.current_char]
            text_surface = self.font.render(partial_text, True, (50, 50, 50))
            self.screen.blit(text_surface, (left_margin, y))
            if self.audio.is_sound_playing("resource/music/sound_effect/typing.mp3") is False:
                self.audio.play_sound("resource/music/sound_effect/typing.mp3")
                

        # 打完後提示點擊
        if self.all_finished:
            tip = self.font.render("（點擊以結束）", True, (150, 150, 150))
            # 水平置中，垂直位置在文字區底部+50
            self.screen.blit(tip, (self.screen.get_width() // 2 - tip.get_width() // 2, 630))
            
    def run(self):
        
        while self.running:
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(self.FPS)
        
            
        
        

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
        self.animator = CharacterAnimator(player.intro, (400, 400), (300, 300))
        font = pygame.font.Font("resource/font/JasonHandwriting3-SemiBold.ttf", 36)
        self.next_week_button = Button(
            self.SCREEN_WIDTH - 200, self.SCREEN_HEIGHT - 100,
            180, 60, "下一週", font, (200, 200, 250), (50, 50, 50), (180, 180, 180))

        excl_img = pygame.image.load("resource/image/event_icon.PNG").convert_alpha()
        self.excl_img = pygame.transform.smoothscale(excl_img, (175, 175))
        self.excl_rect = self.excl_img.get_rect(center=(430, 400))
        self.excl_mask = pygame.mask.from_surface(self.excl_img)
        self.player = player
        self.is_hover = False
        self.hover_scale = 1.1
        if player.name == "Bubu":
            self.animator.frame_delay = 10  # 控制動畫速度

        self.set_icon = pygame.image.load("resource/image/set.png").convert_alpha()
        self.set_icon = pygame.transform.smoothscale(self.set_icon, (80, 80))
        self.set_rect = self.set_icon.get_rect(topleft=(20, 20))
        self.set_hover = False

    def update(self):
        self.animator.update()

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        # 設定按鈕 hover 與點擊
        if self.set_rect.collidepoint(mouse_pos):
            self.set_hover = True
            if mouse_pressed[0]:
                return "SETTING"
        else:
            self.set_hover = False

        # 事件泡泡 hover 與點擊邏輯
        relative_pos = (mouse_pos[0] - self.excl_rect.left, mouse_pos[1] - self.excl_rect.top)
        if (0 <= relative_pos[0] < self.excl_rect.width and
            0 <= relative_pos[1] < self.excl_rect.height and
            self.excl_mask.get_at(relative_pos)):

            if not self.is_hover:
                self.audio.play_sound("resource/music/sound_effect/menu_hover.mp3")
                self.is_hover = True

            if mouse_pressed[0]:
                if self.player.chosen[self.player.week_number] == '0':
                    return "Open Event"
                else:
                    print("this week's event has been done !")
        else:
            self.is_hover = False

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.animator.draw(self.screen)
        self.next_week_button.draw(self.screen)


        if self.set_hover:
            scaled = pygame.transform.scale(self.set_icon, (96, 96))
            rect = scaled.get_rect(center=self.set_rect.center)
            self.screen.blit(scaled, rect.topleft)
        else:
            self.screen.blit(self.set_icon, self.set_rect.topleft)

        if self.player.chosen[self.player.week_number] == '0':
            if self.is_hover:
                scaled_img = pygame.transform.smoothscale(
                    self.excl_img,
                    (int(self.excl_img.get_width() * self.hover_scale),
                     int(self.excl_img.get_height() * self.hover_scale))
                )
                scaled_rect = scaled_img.get_rect(center=self.excl_rect.center)
                self.screen.blit(scaled_img, scaled_rect)

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

            result = self.update()

            # ✅ 如果進入設定畫面
            if result == "SETTING":
                from UI.set_scene import SetScene
                while True:
                    set_scene = SetScene(self.screen)
                    setting_result = set_scene.run()
                    print(f"設定場景回傳：{setting_result}")
                    if setting_result == "BACK":
                        break  # 跳出設定畫面，繼續 MainScene 畫面
                    elif setting_result == "QUIT":
                        return "Quit"
                    else:
                        print("設定中執行其他操作（可擴充）")

            elif result is not None:
                return result

            self.draw()
            pygame.display.flip()
            self.clock.tick(self.FPS)

        return None


import pygame
import os
from UI.components.character_animator import CharacterAnimator
from UI.components.button import Button
from UI.components.audio_manager import AudioManager
from UI.components.base_scene import BaseScene


def blur_surface(surface, amount=4):
    small = pygame.transform.smoothscale(surface, (surface.get_width()//amount, surface.get_height()//amount))
    return pygame.transform.smoothscale(small, surface.get_size())


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

        # event_icon
        excl_img = pygame.image.load("resource/image/event_icon.PNG").convert_alpha()
        self.excl_img = pygame.transform.smoothscale(excl_img, (175, 175))
        self.excl_rect = self.excl_img.get_rect(center=(1100, 580))
        self.excl_mask = pygame.mask.from_surface(self.excl_img)

        # 設定 set.png
        set_img = pygame.image.load("resource/image/set.png").convert_alpha()
        self.set_img = pygame.transform.smoothscale(set_img, (70, 70))
        self.set_rect = self.set_img.get_rect(topleft=(20, 20))

        self.player = player
        self.is_hover = False
        self.set_hover = False
        self.hover_scale = 1.1

    def update(self):
        self.animator.update()
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        # 🛠️ SET 按鈕偵測
        if self.set_rect.collidepoint(mouse_pos):
            self.set_hover = True
            if mouse_pressed[0]:
                return "SETTING"
        else:
            self.set_hover = False

        # 📌 event_icon 判定
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
        self.screen.blit(self.set_img, self.set_rect.topleft)

        if self.player.chosen[self.player.week_number] == '0':
            if self.is_hover:
                scaled_img = pygame.transform.smoothscale(
                    self.excl_img,
                    (int(self.excl_img.get_width() * self.hover_scale),
                     int(self.excl_img.get_height() * self.hover_scale))
                )
                scaled_rect = scaled_img.get_rect(center=self.excl_rect.center)
                self.screen.blit(scaled_img, scaled_rect)
            else:
                self.screen.blit(self.excl_img, self.excl_rect)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "Quit"
                if self.next_week_button.handle_event(event):
                    return "Next Story"

            result = self.update()

            if result == "SETTING":
                from UI.set_scene import SetScene
                screenshot = self.screen.copy()
                blurred_bg = blur_surface(screenshot)
                set_scene = SetScene(self.screen, blurred_bg)
                setting_result = set_scene.run()
                print(f"設定場景回傳：{setting_result}")
                if setting_result == "BACK":
                    continue
                elif setting_result == "QUIT":
                    return "Quit"

            elif result is not None:
                return result

            self.draw()
            pygame.display.flip()
            self.clock.tick(self.FPS)

        return None


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
            180, 60,"下一週", font)

        excl_img = pygame.image.load("resource/image/event_icon.PNG").convert_alpha()
        self.excl_img = pygame.transform.smoothscale(excl_img, (100, 100))
        self.excl_rect = self.excl_img.get_rect(center=(500, 500))
        self.excl_mask = pygame.mask.from_surface(self.excl_img)
        self.player = player
        self.is_hover = False      # 是否目前 hover 狀態
        self.hover_scale = 1.1


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

    

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.next_week_button.draw(self.screen)
        self.animator.draw(self.screen)

        # 根據 hover 狀態決定顯示原圖或放大圖
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
            if self.update()!= None :
                return self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(self.FPS)
        return None


 
   
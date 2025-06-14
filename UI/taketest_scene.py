from UI.components.base_scene import BaseScene
from UI.components.audio_manager import AudioManager
from UI.components.character_animator import CharacterAnimator

import pygame

class TakeTestScene(BaseScene):
    def __init__(self, screen, player):
        super().__init__(screen)
        self.player = player
        
        player.get_midterm()  if player.week_number == 8 else player.get_final()
        # 背景
        self.background = pygame.image.load("resource/image/background_intro.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, self.screen.get_size())
        self.background.set_alpha(100)
        self.overlay_surface = pygame.Surface(screen.get_size()).convert_alpha()
        self.overlay_alpha = 0

        # 字型設定
        self.font = pygame.font.Font("resource/font/JasonHandwriting3-SemiBold.ttf", 36)
        self.font_desc = pygame.font.Font("resource/font/JasonHandwriting3-Regular.ttf", 28)


        self.animator = CharacterAnimator(player.testing, (900, 50), (220, 200))

    def update(self):
        # 更新動畫
        self.animator.update()

        # 更新背景透明度
        if self.overlay_alpha < 255:
            self.overlay_alpha = min(255, self.overlay_alpha + 5)
        self.overlay_surface.fill((0, 0, 0, self.overlay_alpha))

    def draw(self, screen):
        # 繪製背景
        screen.blit(self.background, (0, 0))

        # 繪製動畫
        self.animator.draw(screen)

        # 繪製角色名稱
        name_surface = self.font.render(self.player.chname, True, (255, 255, 255))
        screen.blit(name_surface, (50, 50))

        # 繪製角色介紹
        desc_surface = self.font_desc.render(self.player.intro, True, (255, 255, 255))
        screen.blit(desc_surface, (50, 100))

        # 繪製透明遮罩
        screen.blit(self.overlay_surface, (0, 0))


    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                self.handle_event(event)

            self.update()
            self.draw(self.screen)
            pygame.display.update()
import pygame
import os
import json
from UI.components.character_animator import CharacterAnimator
from UI.components.button import Button
from UI.components.base_scene import BaseScene


class MainScene(BaseScene):
    def __init__(self, screen, player):
        super().__init__(screen)
        # 背景圖片
        self.background = pygame.image.load("resource/image/background_intro.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, self.screen.get_size())
        self.animator = CharacterAnimator(player.intro, (400, 400),(300, 300))  # 角色動畫在右側
        self.next_week_button = Button( 
            self.SCREEN_WIDTH - 200, self.SCREEN_HEIGHT - 100,
            180, 60,"下一週", "resource/font/JasonHandwriting3-SemiBold.ttf",
        )
       
        
    def update(self):
        self.animator.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "Quit"
                    
            if self.next_week_button.handle_event(event) :
                return "Next Story"

                    
               

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.next_week_button.draw(self.screen)
        self.animator.draw(self.screen)
        
  


 
   
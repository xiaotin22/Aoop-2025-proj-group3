import pygame
import os
import json
from UI.components.character_animator import CharacterAnimator
from UI.components.button import Button
from UI.components.story_manager import play_week_story


class MainScene():
    def __init__(self, screen, player, anim_folder ):
        self.screen = screen
        self.player = player
        self.running = True
        self.SCREEN_HEIGHT = 800
        self.SCREEN_WIDTH = 1200
        self.clock = pygame.time.Clock()
        self.hover_sound = pygame.mixer.Sound("resource/music/sound_effect/menu_hover.mp3")
        # 背景圖片
        self.background = pygame.image.load("resource/image/background_intro.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, self.screen.get_size())
        self.animator = CharacterAnimator(anim_folder, (400, 400),(300, 300))  # 角色動畫在右側
        self.next_week_button = Button( 
            self.SCREEN_WIDTH - 200, self.SCREEN_HEIGHT - 100,
            180, 60,"下一週"
        )
       
        
    def update(self):
        self.animator.update()
        

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.next_week_button.draw(self.screen)
        self.animator.draw(self.screen)

    def run(self):
        with open('event/event.json', 'r', encoding='utf-8') as f:
            story_dict = json.load(f)
        current_week = 1
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif self.next_week_button.handle_event(event):
                    print("Button clicked!")
                    if current_week <= 16:
                        current_week = play_week_story(self.screen, story_dict, current_week)

            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
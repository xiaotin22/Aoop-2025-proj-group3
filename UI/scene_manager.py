import pygame
import os

class SceneManager:
    def __init__(self, start_scene):
        self.current_scene = start_scene

    def switch_to(self, new_scene):
        self.current_scene = new_scene

    def update(self):
        if self.current_scene:
            self.current_scene.update()

    def draw(self, screen):
        if self.current_scene:
            self.current_scene.draw(screen)

    def handle_event(self, event):
        if self.current_scene:
            self.current_scene.handle_event(event)
            

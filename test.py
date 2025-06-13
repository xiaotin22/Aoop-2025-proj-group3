import pygame
from UI.components.base_scene import BaseScene
from UI.components.audio_manager import AudioManager
from UI.components.character_animator import CharacterAnimator
from UI.lucky_wheel import LuckyWheel


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Game Start")

    # 幸運輪場景
    options = ["獎品1", "獎品2", "獎品3", "獎品4"," 獎品5"]
    lucky_wheel = LuckyWheel(screen, options)

    lucky_wheel.font = pygame.font.Font("resource/font/JasonHandwriting3-Regular.ttf", 36)
    lucky_wheel.run()

    pygame.quit()
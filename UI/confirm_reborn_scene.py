import pygame
from UI.components.base_scene import BaseScene

class ConfirmRebornScene(BaseScene):
    def __init__(self, screen):
        super().__init__(screen)
        self.font = pygame.font.Font("resource/font/ChenYuluoyan-Thin-Monospaced.ttf", 48)

        self.title = "人生無法重來，但可以重新投胎："
        self.yes_rect = pygame.Rect(400, 500, 150, 80)
        self.no_rect = pygame.Rect(650, 500, 150, 80)

    def run(self):
        while self.running:
            self.screen.fill((255, 255, 255))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.yes_rect.collidepoint(event.pos):
                        return "REBORN"
                    elif self.no_rect.collidepoint(event.pos):
                        return "BACK"

            # 畫提示文字
            text_surface = self.font.render(self.title, True, (0, 0, 0))
            self.screen.blit(text_surface, (self.SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 300))

            # 畫按鈕
            pygame.draw.rect(self.screen, (150, 180, 250), self.yes_rect, border_radius=12)
            pygame.draw.rect(self.screen, (200, 200, 200), self.no_rect, border_radius=12)

            yes_text = self.font.render("是", True, (0, 0, 0))
            no_text = self.font.render("否", True, (0, 0, 0))
            self.screen.blit(yes_text, self.yes_rect.move(
                (self.yes_rect.width - yes_text.get_width()) // 2,
                (self.yes_rect.height - yes_text.get_height()) // 2
            ))
            self.screen.blit(no_text, self.no_rect.move(
                (self.no_rect.width - no_text.get_width()) // 2,
                (self.no_rect.height - no_text.get_height()) // 2
            ))

            pygame.display.flip()
            self.clock.tick(self.FPS)


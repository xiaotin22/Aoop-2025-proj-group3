import pygame
from UI.components.base_scene import BaseScene
from UI.components.image_button import ImageButton

class ConfirmScene(BaseScene):
    def __init__(self, screen):
        super().__init__(screen)

        self.message_font = pygame.font.Font("resource/font/ChenYuluoyan-Thin-Monospaced.ttf", 42)
        self.message = "人生無法重來，但可以重新投胎："

        font = pygame.font.Font("resource/font/ChenYuluoyan-Thin-Monospaced.ttf", 32)

        # 是 / 否 按鈕（放在 __init__ 裡）
        self.button_yes = ImageButton("resource/image/red_button.png", (400, 400), text="是", font=font)
        self.button_no = ImageButton("resource/image/red_button.png", (700, 400), text="否", font=font)


    def run(self):
        while self.running:
            self.screen.fill((245, 235, 210))

            # 顯示訊息
            msg_surface = self.message_font.render(self.message, True, (80, 60, 50))
            msg_rect = msg_surface.get_rect(center=(self.SCREEN_WIDTH // 2, 220))
            self.screen.blit(msg_surface, msg_rect)

            # 更新與繪製按鈕
            self.yes_button.update()
            self.no_button.update()
            self.yes_button.draw(self.screen)
            self.no_button.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.yes_button.is_clicked(event):
                        return "RESTART"
                    elif self.no_button.is_clicked(event):
                        return "BACK"

            pygame.display.flip()
            self.clock.tick(self.FPS)

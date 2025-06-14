import pygame
import pygame.gfxdraw
import os

class MainScene:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.running = True

        # 🖼️ 圖片載入
        self.background = pygame.image.load("resource/image/background_intro.png").convert()
        self.set_icon = pygame.image.load("resource/image/set.png").convert_alpha()
        self.set_page = pygame.image.load("resource/image/set_page.png").convert_alpha()
        self.back_icon = pygame.image.load("resource/image/back.png").convert_alpha()

        # 📍 設定按鈕與返回按鈕的位置
        self.set_rect = self.set_icon.get_rect(topleft=(20, 20))
        self.back_rect = self.back_icon.get_rect(topleft=(20, 20))

        self.show_settings = False  # 判斷目前是否為設定頁

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            self.screen.blit(self.background, (0, 0))

            if self.show_settings:
                # 模糊背景並畫出設定頁
                self.draw_blurred_background()
                self.screen.blit(self.set_page, (0, 0))
                self.draw_hover_button(self.back_icon, self.back_rect)
            else:
                # ⚙️ 畫出設定按鈕
                self.draw_hover_button(self.set_icon, self.set_rect)

            pygame.display.update()
            clock.tick(60)
            self.handle_events()

        return "Next"  # 結束場景回傳結果

    def draw_hover_button(self, image, rect):
        mouse_pos = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_pos):
            # 滑鼠移上去會放大
            scaled = pygame.transform.scale(image, (int(rect.width * 1.2), int(rect.height * 1.2)))
            new_rect = scaled.get_rect(center=rect.center)
            self.screen.blit(scaled, new_rect.topleft)
        else:
            self.screen.blit(image, rect.topleft)

    def draw_blurred_background(self):
        # 把當前畫面抓下來模糊
        snapshot = self.screen.copy()
        small = pygame.transform.smoothscale(snapshot, (self.screen.get_width()//10, self.screen.get_height()//10))
        blurred = pygame.transform.smoothscale(small, self.screen.get_size())
        self.screen.blit(blurred, (0, 0))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if self.show_settings:
                    if self.back_rect.collidepoint(mouse_pos):
                        self.show_settings = False  # 回主畫面
                else:
                    if self.set_rect.collidepoint(mouse_pos):
                        self.show_settings = True  # 進入設定畫面

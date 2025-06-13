import pygame
from UI.components.base_scene import BaseScene
from UI.components.audio_manager import AudioManager
from UI.components.character_animator import CharacterAnimator

class SoundControlScene(BaseScene):
    def __init__(self, screen):
        super().__init__(screen)
        self.audio = AudioManager.get_instance()
        self.titlefont = pygame.font.Font("resource/font/JasonHandwriting3-SemiBold.ttf", 70)
        self.font = pygame.font.Font("resource/font/JasonHandwriting3-Regular.ttf", 48)

        # 滑桿參數
        self.slider_width = 300
        self.slider_height = 10
        self.knob_radius = 15

        self.bgm_volume = self.audio.volume
        self.sfx_volume = self.audio.sound_volume

        # 滑桿位置
        self.bgm_slider_rect = pygame.Rect(300, 300, self.slider_width, self.slider_height)
        self.sfx_slider_rect = pygame.Rect(300, 450, self.slider_width, self.slider_height)

        self.dragging_bgm = False
        self.dragging_sfx = False
        self.animator = CharacterAnimator("resource/gif/bubu_playgame_frames", (850, 50), (300, 300))

    def handle_event(self, event):
        super().handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._knob_rect(self.bgm_slider_rect, self.bgm_volume).collidepoint(event.pos):
                self.dragging_bgm = True
            elif self._knob_rect(self.sfx_slider_rect, self.sfx_volume).collidepoint(event.pos):
                self.dragging_sfx = True
                # 按下音效滑桿的 knob 時播放一聲音效
                self.audio.play_sound("resource/music/sound_effect/menu_hover.mp3")

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging_bgm = False
            self.dragging_sfx = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging_bgm:
                self.bgm_volume = self._get_volume_from_mouse(event.pos[0], self.bgm_slider_rect)
                self.audio.set_bgm_volume(self.bgm_volume)
            elif self.dragging_sfx:
                self.sfx_volume = self._get_volume_from_mouse(event.pos[0], self.sfx_slider_rect)
                self.audio.set_sound_volume(self.sfx_volume)

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.running = False

    def _get_volume_from_mouse(self, mouse_x, slider_rect):
        rel_x = max(slider_rect.left, min(mouse_x, slider_rect.right))
        return (rel_x - slider_rect.left) / self.slider_width

    def _knob_rect(self, slider_rect, volume):
        x = slider_rect.left + int(volume * self.slider_width)
        y = slider_rect.centery
        return pygame.Rect(x - self.knob_radius, y - self.knob_radius, self.knob_radius * 2, self.knob_radius * 2)

    def update(self):
        self.animator.update()

    def draw(self, screen):
        screen.fill((40, 40, 60))
        
        # 標題
        title = self.titlefont.render("音量設定", True, (255, 255, 255))
        screen.blit(title, (self.SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        # BGM 音量滑桿
        self._draw_slider(screen, self.bgm_slider_rect, self.bgm_volume, "背景音樂")

        # SFX 音效滑桿
        self._draw_slider(screen, self.sfx_slider_rect, self.sfx_volume, "音效")

        # 提示
        hint = self.font.render("按 Esc 返回", True, (200, 200, 200))
        screen.blit(hint, (self.SCREEN_WIDTH - 300, self.SCREEN_HEIGHT - 60))
        self.animator.draw(screen)

    def _draw_slider(self, screen, rect, volume, label):
        # 標籤
        label_surface = self.font.render(f"{label}: {int(volume * 100)}%", True, (255, 255, 255))
        screen.blit(label_surface, (rect.left, rect.top - 60))

        # 滑桿底座
        pygame.draw.rect(screen, (180, 180, 180), rect)
        # 滑桿前景
        filled_rect = pygame.Rect(rect.left, rect.top, int(rect.width * volume), rect.height)
        pygame.draw.rect(screen, (120, 200, 250), filled_rect)
        # 圓形 knob
        knob_x = rect.left + int(volume * rect.width)
        pygame.draw.circle(screen, (250, 250, 250), (knob_x, rect.centery), self.knob_radius)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)

            self.update()
            self.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(self.FPS)

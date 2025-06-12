import pygame

class AudioManager:
    _instance = None  # 單例

    def __init__(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init()
            
        if AudioManager._instance is not None:
            raise Exception("AudioManager 是單例，請使用 get_instance() 取得")
        pygame.mixer.init()
        self.current_bgm = None
        self.volume = 0.5
        AudioManager._instance = self

    @staticmethod
    def get_instance():
        if AudioManager._instance is None:
            AudioManager()
        return AudioManager._instance

    # 播放背景音樂
    def play_bgm(self, filepath, loop=-1):
        if self.current_bgm != filepath:
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(loop)
            self.current_bgm = filepath

    # 停止背景音樂
    def stop_bgm(self):
        pygame.mixer.music.stop()
        self.current_bgm = None

    # 暫停背景音樂
    def pause_bgm(self):
        pygame.mixer.music.pause()

    # 恢復背景音樂
    def resume_bgm(self):
        pygame.mixer.music.unpause()

    # 設定背景音樂音量
    def set_bgm_volume(self, volume):
        self.volume = volume
        pygame.mixer.music.set_volume(volume)

    # 播放音效
    def play_sound(self, filepath):
        sound = pygame.mixer.Sound(filepath)
        sound.set_volume(self.volume)
        sound.play()

import pygame
import random
import math

class FloatingEmoji:
    def __init__(self, image, start_pos, duration=  5000):
        self.original_image = image
        self.start_pos = pygame.Vector2(start_pos)
        self.pos = self.start_pos.copy()
        self.start_time = pygame.time.get_ticks()
        self.duration = duration

        # 飄向中心＋隨機角度與速度（更快）
        center = pygame.Vector2(600, 400)
        direction = center - self.pos
        if direction.length() > 0:
            direction = direction.normalize()
        random_angle = random.uniform(-0.6, 0.6)
        self.velocity = direction.rotate_rad(random_angle) * random.uniform(5, 10)

        # 初始旋轉角度與速度
        self.angle = random.uniform(0, 360)
        self.angular_speed = random.uniform(-3,  3)  # 隨機旋轉速度

        # 初始縮放
        self.scale = 1.0

    def update(self):
        elapsed = pygame.time.get_ticks() - self.start_time
        t = elapsed / self.duration  # 0 ~ 1

        self.pos += self.velocity
        self.angle += self.angular_speed
        self.scale = max(0.6, 1.0 - t * 0.4)  # 逐漸縮小

    def draw(self, screen):
        elapsed = pygame.time.get_ticks() - self.start_time
        t = elapsed / self.duration
        alpha = max(0, 255 * (1 - t))  # 逐漸透明

        # 旋轉 & 縮放圖片
        size = self.original_image.get_size()
        new_size = (int(size[0] * self.scale), int(size[1] * self.scale))
        image = pygame.transform.rotozoom(self.original_image, self.angle, self.scale)
        image.set_alpha(int(alpha))

        # 中心對齊
        rect = image.get_rect(center=self.pos)
        screen.blit(image, rect)

    def is_expired(self):
        return pygame.time.get_ticks() - self.start_time > self.duration

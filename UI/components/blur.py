import pygame
import pygame.surfarray

def fast_blur(surface, scale=0.25):
    """將 surface 進行快速模糊：先縮小再放大"""
    size = surface.get_size()
    small_size = (int(size[0] * scale), int(size[1] * scale))
    small_surface = pygame.transform.smoothscale(surface, small_size)
    blurred_surface = pygame.transform.smoothscale(small_surface, size)
    return blurred_surface


import pygame

from settings import *

# Seperate file for the breaking animation of the bricks
class PlatformDebris(object):
    
    def __init__(self, x, y):
        self.image = pygame.image.load('images/block_debris0.png').convert_alpha()

        self.rectangles = [
            pygame.Rect(x - 20, y + 16, 16, 16),
            pygame.Rect(x - 20, y - 16, 16, 16),
            pygame.Rect(x + 20, y + 16, 16, 16),
            pygame.Rect(x + 20, y - 16, 16, 16)
        ]
        self.vy = -4
        self.rect = None

    # Causes particles to fall and phase through the floor
    def update(self, main):
        self.vy += gravity

        for i in range(len(self.rectangles)):
            self.rectangles[i].y += self.vy
            if i < 2:
                self.rectangles[i].x -= 1
            else:
                self.rectangles[i].x += 1

        if self.rectangles[1].y > main.get_map().map_size[1] * 32:
            main.get_map().debris.remove(self)
    
    # Draws particles once the brick is broken
    def render(self, main):
        for rect in self.rectangles:
            self.rect = rect
            main.screen.blit(self.image, main.get_map().get_camera().apply(self))

import pygame

from settings import *


class PlatformDebris(object):
    """

    Debris which appears when you destroy a brick block.

    """
    def __init__(self, x, y):
        self.image = pygame.image.load('images/block_debris0.png').convert_alpha()

        # 4 different parts
        self.rectangles = [
            pygame.Rect(x - 20, y + 16, 16, 16),
            pygame.Rect(x - 20, y - 16, 16, 16),
            pygame.Rect(x + 20, y + 16, 16, 16),
            pygame.Rect(x + 20, y - 16, 16, 16)
        ]
        self.vy = -4
        self.rect = None

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

    def render(self, main):
        for rect in self.rectangles:
            self.rect = rect
            main.screen.blit(self.image, main.get_map().get_camera().apply(self))

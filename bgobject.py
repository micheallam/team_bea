import pygame


class BGObject(object):
    # Parent class for background objects
    def __init__(self, x, y, image):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.image = image
        # Type BGObject that Entity compares to
        self.type = 'BGObject'

    def render(self, main):
        main.screen.blit(self.image, main.get_map().get_camera().apply(self))
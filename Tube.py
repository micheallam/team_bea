import pygame


class Tube(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('images/tube.png').convert_alpha()
        length = (12 - y) * 32
        self.image = self.image.subsurface(0, 0, 64, length)
        self.rect = pygame.Rect(x * 32, y * 32, 64, length)

    def render(self, main):
        main.screen.blit(self.image, main.get_map().get_camera().apply(self))

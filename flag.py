import pygame


class Flag(object):
    def __init__(self, x, y):
        self.rect = None

        self.flag_offset = 0
        self.flag_spawn = False

        self.pole_image = pygame.image.load('images/flag_pillar.png').convert_alpha()
        self.pole_rect = pygame.Rect(x + 8, y, 16, 304)

        self.flag_image = pygame.image.load('images/flag.png').convert_alpha()
        self.flag_rect = pygame.Rect(x - 18, y + 16, 32, 32)

    def move_flag_down(self):
        self.flag_offset += 3
        self.flag_rect.y += 3

        if self.flag_offset >= 255:
            self.flag_spawn = True

    def render(self, main):
        self.rect = self.pole_rect
        main.screen.blit(self.pole_image, main.get_map().get_camera().apply(self))

        self.rect = self.flag_rect
        main.screen.blit(self.flag_image, main.get_map().get_camera().apply(self))
import pygame

class CoinHit(object):
    # The coins that show up when you hit a block
    def __init__(self, x_pos, y_pos):
        self.rect = pygame.Rect(x_pos, y_pos, 16, 28)

        self.vy = -2
        self.y_offset = 0
        self.moving_up = True

        self.current_image = 0
        self.image_tick = 0
        self.images = [
            pygame.image.load('images/coin_an0.png').convert_alpha(),
            pygame.image.load('images/coin_an1.png').convert_alpha(),
            pygame.image.load('images/coin_an2.png').convert_alpha(),
            pygame.image.load('images/coin_an3.png').convert_alpha()
        ]

    def update(self, main):
        self.image_tick += 1

        if self.image_tick % 15 == 0:
            self.current_image += 1

        if self.current_image == 4:
            self.current_image = 0
            self.image_tick = 0

        if self.moving_up:
            self.y_offset += self.vy
            self.rect.y += self.vy
            if self.y_offset < -50:
                self.moving_up = False
                self.vy = -self.vy
        else:
            self.y_offset += self.vy
            self.rect.y += self.vy
            if self.y_offset == 0:
                main.get_map().debris.remove(self)

    def render(self, main):
        main.screen.blit(self.images[self.current_image], main.get_map().get_camera().apply(self))
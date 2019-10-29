import pygame

from entity import Entity
from settings import *


class Mushroom(Entity):
    def __init__(self, x, y, move_direction):
        super().__init__()

        self.rect = pygame.Rect(x, y, 32, 32)

        if move_direction:
            self.x_V = 1
        else:
            self.x_V = -1

        self.spawned = False
        self.spawn_y = 0
        self.image = pygame.image.load('images/mushroom.png').convert_alpha()

    def check_collision_with_player(self, main):
        if self.rect.colliderect( main.get_map().get_player().rect):
            main.get_map().get_player().set_powerlvl(2, main)
            main.get_map().get_mobs().remove(self)

    def die(self, main, instantly, crushed):
        main.get_map().get_mobs().remove(self)

    def spawn_animation(self):
        self.spawn_y -= 1
        self.rect.y -= 1

        if self.spawn_y == - 32:
            self.spawned = True

    def update(self, main):
        if self.spawned:
            if not self.on_ground:
                self.y_V += GRAVITY

            blocks = main.get_map().get_blocks_for_collision(self.rect.x // 32, self.rect.y // 32)
            self.update_x_pos(blocks)
            self.update_y_pos(blocks)

            self.check_map_borders(main)
        else:
            self.spawn_animation()

    def render(self, main):
        main.screen.blit(self.image, main.get_map().get_camera().apply(self))
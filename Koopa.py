import pygame

from entity import Entity
from settings import *


class Koopa(Entity):
    def __init__(self, x, y, move_direction):
        super().__init__()
        self.rect = pygame.Rect(x, y, 32, 46)

        self.move_direction = move_direction

        if move_direction:
            self.vx = 1
        else:
            self.vx = -1

        self.current_image = 0
        self.timer = 0
        self.images = [
            pygame.image.load('images/koopa_0.png').convert_alpha(),
            pygame.image.load('images/koopa_1.png').convert_alpha(),
            pygame.image.load('images/koopa_dead.png').convert_alpha()
        ]
        self.images.append(pygame.transform.flip(self.images[0], 180, 0))
        self.images.append(pygame.transform.flip(self.images[1], 180, 0))
        self.images.append(pygame.transform.flip(self.images[2], 0, 180))

    def check_collision_with_player(self, main):
        if self.collision:
            if self.rect.colliderect(main.get_map().get_player().rect):
                if self.state != -1:
                    if main.get_map().get_player().vy > 0:
                        self.change_state(main)
                        main.get_sound().play('kill_mob', 0, 0.5)
                        main.get_map().get_player().reset_jump()
                        main.get_map().get_player().jump_on_mob()
                    else:
                        if not main.get_map().get_player().unkillable:
                            main.get_map().get_player().Mario_size(0, main)

    def check_collision_with_mobs(self, main):
        for mob in main.get_map().get_mobs():
            if mob is not self:
                if self.rect.colliderect(mob.rect):
                    if mob.collision:
                        mob.die(main, instantly=False, stomped=False)

    def die(self, main, instantly, stomped):
        if not instantly:
            main.get_map().get_player().add_score(main.get_map().m_points)
            main.get_map().spawn_score_text(self.rect.x + 16, self.rect.y)
            self.state = -1
            self.vy = -4
            self.current_image = 5
        else:
            main.get_map().get_mobs().remove(self)

    def change_state(self, main):
        self.state += 1
        self.current_image = 2

        if self.rect.h == 46:
            self.vx = 0
            self.rect.h = 32
            self.rect.y += 14
            main.get_map().get_player().add_score(100)
            main.get_map().spawn_score_text(self.rect.x + 16, self.rect.y, score=100)

        elif self.state == 2:
            main.get_map().get_player().add_score(100)
            main.get_map().spawn_score_text(self.rect.x + 16, self.rect.y, score=100)

            if main.get_map().get_player().rect.x - self.rect.x <= 0:
                self.vx = 6
            else:
                self.vx = -6

        elif self.state == 3:
            self.die(main, instantly=False, stomped=False)

    def update_image(self):
        self.timer += 1

        if self.vx > 0:
            self.move_direction = True
        else:
            self.move_direction = False

        if self.timer == 35:
            if self.move_direction:
                self.current_image = 4
            else:
                self.current_image = 1
        elif self.timer == 70:
            if self.move_direction:
                self.current_image = 3
            else:
                self.current_image = 0
            self.timer = 0

    def update(self, main):
        if self.state == 0:
            self.update_image()

            if not self.on_ground:
                self.vy += gravity

            blocks = main.get_map().get_blocks_for_collision(self.rect.x // 32, (self.rect.y - 14) // 32)
            self.move_horizontally(blocks)
            self.move_vertically(blocks)

            self.check_borders(main)

        elif self.state == 1:
            blocks = main.get_map().get_blocks_for_collision(self.rect.x // 32, self.rect.y // 32)
            self.move_horizontally(blocks)
            self.move_vertically(blocks)

            self.check_borders(main)

        elif self.state == 2:
            if not self.on_ground:
                self.vy += gravity

            blocks = main.get_map().get_blocks_for_collision(self.rect.x // 32, self.rect.y // 32)
            self.move_horizontally(blocks)
            self.move_vertically(blocks)

            self.check_borders(main)
            self.check_collision_with_mobs(main)

        elif self.state == -1:
            self.rect.y += self.vy
            self.vy += gravity

            self.check_borders(main)

    def render(self, main):
        main.screen.blit(self.images[self.current_image], main.get_map().get_camera().apply(self))

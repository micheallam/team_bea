import pygame

from entity import Entity
from settings import *


class Goombas(Entity):
    def __init__(self, x, y, move_direction):
        super().__init__()
        self.rect = pygame.Rect(x, y, 32, 32)

        if move_direction:
            self.x_V = 1
        else:
            self.x_V = -1

        self.stomped = False

        self.current_image = 0
        self.frame = 0
        self.images = [
            pygame.image.load('images/goombas_0.png').convert_alpha(),
            pygame.image.load('images/goombas_1.png').convert_alpha(),
            pygame.image.load('images/goombas_dead.png').convert_alpha()
        ]
        self.images.append(pg.transform.flip(self.images[0], 0, 180))

    def die(self, main, instantly, stomped):
        if not instantly:
            main.get_map().get_player().add_score(main.get_map().score_for_killing_mob)
            main.get_map().spawn_score_text(self.rect.x + 16, self.rect.y)

            if stomped:
                self.stomped = True
                self.frame = 0
                self.current_image = 2
                self.state = -1
                main.get_sound().play('kill_mob', 0, 0.5)
                self.collision = False

            else:
                self.y_V = -4
                self.current_image = 3
                main.get_sound().play('shot', 0, 0.5)
                self.state = -1
                self.collision = False

        else:
            main.get_map().get_mobs().remove(self)

    def check_collision_with_player(self, main):
        if self.collision:
            if self.rect.colliderect(main.get_map().get_player().rect):
                if self.state != -1:
                    if main.get_map().get_player().y_V > 0:
                        self.die(main, instantly=False, stomped=True)
                        main.get_map().get_player().reset_jump()
                        main.get_map().get_player().jump_on_mob()
                    else:
                        if not main.get_map().get_player().unkillable:
                            main.get_map().get_player().Mario_size(0, main)

    def update_image(self):
        self.frame += 1
        if self.frame == 14:
            self.current_image = 1
        elif self.frame == 28:
            self.current_image = 0
            self.frame = 0

    def update(self, main):
        if self.state == 0:
            self.update_image()

            if not self.on_ground:
                self.y_V += GRAVITY

            blocks = main.get_map().get_blocks_for_collision(int(self.rect.x // 32), int(self.rect.y // 32))
            self.update_x_pos(blocks)
            self.update_y_pos(blocks)

            self.check_map_borders(main)

        elif self.state == -1:
            if self.stomped:
                self.frame += 1
                if self.frame == 50:
                    main.get_map().get_mobs().remove(self)
            else:
                self.y_V += GRAVITY
                self.rect.y += self.y_V
                self.check_map_borders(main)

    def render(self, main):
        main.screen.blit(self.images[self.current_image], main.get_map().get_camera().apply(self))

import pygame

from entity import Entity


class Flower(Entity):
    def __init__(self, x, y):
        super().__init__()

        self.rect = pygame.Rect(x, y, 32, 32)
        self.spawned = False
        self.spawned_y = 0

        self.current_image = 0
        self.timer = 0
        self.images = (
            pygame.image.load('images/flower0.png').convert_alpha(),
            pygame.image.load('images/flower1.png').convert_alpha(),
            pygame.image.load('images/flower2.png').convert_alpha(),
            pygame.image.load('images/flower3.png').convert_alpha()
        )

    def check_collision_with_player(self, main):
        if self.rect.colliderect(main.get_map().get_player().rect):
            main.get_map().get_player().set_size(3, main)
            main.get_map().get_mobs().remove(self)

    def update_image(self):
        self.timer += 1

        if self.timer == 60:
            self.timer = 0
            self.current_image = 0

        elif self.timer % 15 == 0:
            self.current_image += 1

    def spawn_animation(self):
        self.spawned_y -= 1
        self.rect.y -= 1

        if self.spawned_y == -32:
            self.spawned = True

    def update(self, main):
        if self.spawned:
            self.update_image()
        else:
            self.spawn_animation()

    def render(self, main):
        main.screen.blit(self.images[self.current_image], main.get_map().get_camera().apply(self))

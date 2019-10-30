import pygame

from settings import *


class Fireball(object):
    def __init__(self, x, y, move_dir: bool):
        super().__init__()

        self.rect = pygame.Rect(x, y, 16, 16)
        self.frame = 0
        self.direction = move_dir
        self.vx = 5 if move_dir else -5
        self.vy = 0
        
        # Defines images and animation timers
        self.current_image = 0
        self.timer = 0
        self.images = [pygame.image.load('images/fireball.png').convert_alpha()]
        self.images.append(pygame.transform.flip(self.images[0], 0, 90))
        self.images.append(pygame.transform.flip(self.images[0], 90, 90))
        self.images.append(pygame.transform.flip(self.images[0], 90, 0))
        self.images.append(pygame.image.load('images/firework0.png').convert_alpha())
        self.images.append(pygame.image.load('images/firework1.png').convert_alpha())
        self.images.append(pygame.image.load('images/firework2.png').convert_alpha())

# Animates the fire moving ===============================================================================================        
    def update_image(self, main):
        self.timer += 1

        if self.frame == 0:
            if self.timer % 15 == 0:
                self.current_image += 1
                if self.current_image > 3:
                    self.current_image = 0
                    self.timer = 0

        elif self.frame == -1:
            if self.timer % 10 == 0:
                self.current_image += 1
            if self.current_image == 7:
                main.get_map().remove_whizbang(self)

# When fire collides with an object ==================================================================================================                
    def start_boom(self):
        self.vx = 0
        self.vy = 0
        self.current_image = 4
        self.timer = 0
        self.frame = -1

# Moves the fire to the right ======================================================================================================        
    def move_horizontally(self, blocks):
        self.rect.x += self.vx
        for block in blocks:
            if block != 0 and block.type != 'BGObject':
                if pygame.Rect.colliderect(self.rect, block.rect):

                    # Fireball blows up only when collides on x-axis
                    self.start_boom()

 # Bouncing aspect of animation ======================================================================================================                   
    def move_vertically(self, blocks):
        self.rect.y += self.vy
        for block in blocks:
            if block != 0 and block.type != 'BGObject':
                if pygame.Rect.colliderect(self.rect, block.rect):
                    self.rect.bottom = block.rect.top
                    self.vy = -3

 # removes fireball when interacting ===================================================================================================                
    def check_borders(self, main):
        if self.rect.x <= 0:
            main.get_map().remove_whizbang(self)
        elif self.rect.y > 448:
            main.get_map().remove_whizbang(self)

    def move(self, main):
        self.vy += gravity

        blocks = main.get_map().get_blocks_for_collision(self.rect.x // 32, self.rect.y // 32)
        self.move_vertically(blocks)
        self.move_horizontally(blocks)

        self.check_borders(main)

 # Sets kill flags for enemies if collided ======================================================================================================
    def check_collision_with_mobs(self, main):
        for mob in main.get_map().get_mobs():
            if self.rect.colliderect(mob.rect):
                if mob.collision:
                    mob.die(main, instantly=False, stomped=False)
                    self.start_boom()

    def update(self, main):
        if self.frame == 0:
            self.update_image(main)
            self.move(main)
            self.check_collision_with_mobs(main)
        elif self.frame == -1:
            self.update_image(main)

    def render(self, main):
        main.screen.blit(self.images[self.current_image], main.get_map().get_camera().apply(self))

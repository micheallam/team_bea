import pygame

# Parent class for everything
class Entity(object):
    def __init__(self):
        # Image of Entity and position
        self.image = None
        self.rect = None
        # State of the entity
        self.state = 0
        # Variables that control the movement of the Entity
        self.vx = 0 # x_vel delete this
        self.vy = 0 # y_vel delete this
        # Booleans Entity
        self.direction = True
        self.on_ground = False
        self.collision = True

    def move_horizontally(self, blocks):
        self.rect.x += self.vx

        for block in blocks:
            if block != 0 and block.type != 'BGObject':
                if pygame.Rect.colliderect(self.rect, block.rect):
                    if self.vx > 0:
                        self.rect.right = block.rect.right
                        self.vx = -self.vx
                    elif self.vx < 0:
                        self.rect.left = block.rect.right
                        self.vx = -self.vx

    def move_vertically(self, blocks):
        self.rect.y += self.vy

        self.on_ground = False
        for block in blocks:
            if block != 0 and block.type != 'BGObject':
                if pygame.Rect.colliderect(self.rect, block.rect):
                    if self.vy > 0:
                        self.on_ground = True
                        self.rect.bottom = block.rect.top
                        self.vy = 0


    def check_borders(self, main):
        if self.rect.y >= 448:
            # Kill if you drop past border
            self.die(main, True, False)
        if self.rect.x <= 1 and self.vx < 0:
            self.vx = -self.vx

    def die(self, main, instantly, crushed):
        pass

    def render(self, main):
        pass


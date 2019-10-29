import pygame


class Platform(object):
    def __init__(self, x, y, image, type_id):
        self.image = image
        self.rect = pygame.Rect(x, y, 32, 32)

        # 22 - question block
        # 23 - brick block
        self.typeID = type_id

        self.type = 'Platform'

        self.shake = False
        self.hit = True
        self.shakedelay = 0

        if self.typeID == 22:
            self.currentImage = 0
            self.imageTick = 0
            self.isActivated = False
            self.bonus = 'coin'

    def update(self):
        if self.typeID == 22:
            self.imageTick += 1
            if self.imageTick == 50:
                self.currentImage = 1
            elif self.imageTick == 60:
                self.currentImage = 2
            elif self.imageTick == 70:
                self.currentImage = 1
            elif self.imageTick == 80:
                self.currentImage = 0
                self.imageTick = 0

    def shake(self):
        if self.hit:
            self.shakedelay -= 2
            self.rect.y -= 2
        else:
            self.shakedelat += 2
            self.rect.y += 2
        if self.shakedelay == -20:
            self.shakingUp = False
        if self.shakedelay == 0:
            self.shake = False
            self.hit = True

    def spawn_bonus(self, main):
        self.isActivated = True
        self.shake = True
        self.imageTick = 0
        self.currentImage = 3

        if self.bonus == 'mushroom':
            main.get_sound().play('mushroom_appear', 0, 0.5)
            if main.get_map().get_player().powerLVL == 0:
                main.get_map().spawn_mushroom(self.rect.x, self.rect.y)
            else:
                main.get_map().spawn_flower(self.rect.x, self.rect.y)

        elif self.bonus == 'coin':
            main.get_sound().play('coin', 0, 0.5)
            main.get_map().spawn_debris(self.rect.x + 8, self.rect.y - 32, 1)
            main.get_map().get_player().add_coins(1)
            main.get_map().get_player().add_score(200)

    def destroy(self, main):
        main.get_map().spawn_debris(self.rect.x, self.rect.y, 0)
        main.get_map().remove_object(self)

    def render(self, main):

        # Question block
        if self.typeID == 22:
            if not self.isActivated:
                self.update()
            elif self.shake:
                self.shake()
            main.screen.blit(self.image[self.currentImage], main.get_map().get_camera().apply(self))

        # Brick block
        elif self.typeID == 23 and self.shake:
            self.shake()
            main.screen.blit(self.image, main.get_map().get_camera().apply(self))

        else:
            main.screen.blit(self.image, main.get_map().get_camera().apply(self))
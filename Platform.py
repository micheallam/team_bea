import pygame

# Creates the platforms namely the floor
class Platform(object):
    def __init__(self, x, y, image, type_id):
        self.image = image
        self.rect = pygame.Rect(x, y, 32, 32)

        self.typeID = type_id

        self.type = 'Platform'
        
        # Active flags
        self.shaking = False
        self.hit = True
        self.shakedelay = 0

        # Code to recognize it is a question block
        if self.typeID == 22:
            self.currentImage = 0
            self.imageTick = 0
            self.isActivated = False
            self.bonus = 'coin'

    def update(self):
        # Question block passively changes image
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
        # Hitting the block causes it to move up slightly
        if self.hit:
            self.shakedelay -= 2
            self.rect.y -= 2
        else:
            self.shakedelay += 2
            self.rect.y += 2
        if self.shakedelay == -20:
            self.hit = False
        if self.shakedelay == 0:
            self.shaking = False
            self.hit = True

    def spawn_bonus(self, main):
        self.isActivated = True
        self.shaking = True
        self.imageTick = 0
        self.currentImage = 3

        # Mushroom power-up spawn
        if self.bonus == 'mushroom':
            main.get_sound().play('mushroom_appear', 0, 0.5)
            if main.get_map().get_player().size == 0:
                main.get_map().spawn_mushroom(self.rect.x, self.rect.y)
            else:
                main.get_map().spawn_flower(self.rect.x, self.rect.y)
        
        # Creates a coin 
        elif self.bonus == 'coin':
            main.get_sound().play('coin', 0, 0.5)
            main.get_map().spawn_debris(self.rect.x + 8, self.rect.y - 32, 1)
            main.get_map().get_player().add_coins(1)
            main.get_map().get_player().add_score(200)
    
    # Removes object from the screen
    def destroy(self, main):
        main.get_map().spawn_debris(self.rect.x, self.rect.y, 0)
        main.get_map().remove_object(self)

    def render(self, main):

        # Draws Question block
        if self.typeID == 22:
            if not self.isActivated:
                self.update()
            elif self.shaking:
                self.shake()
            main.screen.blit(self.image[self.currentImage], main.get_map().get_camera().apply(self))

        # Draws Brick block
        elif self.typeID == 23 and self.shaking:
            self.shake()
            main.screen.blit(self.image, main.get_map().get_camera().apply(self))

        else:
            main.screen.blit(self.image, main.get_map().get_camera().apply(self))

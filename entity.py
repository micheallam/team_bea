import pygame
from settings import *


# Parent class for everything that is interactable
class Entity(object):
    def __init__(self):
        
        # Image of Entity and position
        self.image = None
        self.rect = None
        
        # State of the entity
        self.state = 0
        
        # Variables that control the movement of the Entity
        self.vx = 0
        self.vy = 0
        
        # Entitiy flags
        self.direction = True
        self.on_ground = False
        self.collision = True

    # Creates movement for the object
    def move_horizontally(self, blocks):
        self.rect.x += self.vx

        for block in blocks:
            if block != 0 and block.type != 'BGObject':
                if pygame.Rect.colliderect(self.rect, block.rect):
                    if self.vx > 0:
                        self.rect.right = block.rect.left
                        self.vx = -self.vx
                    elif self.vx < 0:
                        self.rect.left = block.rect.right
                        self.vx = -self.vx

    # Allows the blocks to move up when hit
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

    # Falling through a pit
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

# Mushroom object =====================================================================
class Mushroom(Entity):
    def __init__(self, x, y, move_direction):
        super().__init__()

        self.rect = pygame.Rect(x, y, 32, 32)

        if move_direction:
            self.vx = 1
        else:
            self.vx = -1
        
        # Flags to spawn the mushroom
        self.spawned = False
        self.spawn_y = 0
        self.image = pygame.image.load('images/mushroom.png').convert_alpha()

    # Mario eating the mushroom
    def check_collision_with_player(self, main):
        if self.rect.colliderect( main.get_map().get_player().rect):
            main.get_map().get_player().set_size(2, main)
            main.get_map().get_mobs().remove(self)

    def die(self, main, instantly, crushed):
        main.get_map().get_mobs().remove(self)

    # Mushroom moves up from the block one unit at a time until it fully spawns and starts to move
    def spawn_animation(self):
        self.spawn_y -= 1
        self.rect.y -= 1

        if self.spawn_y == - 32:
            self.spawned = True

    # allows it to fall off ledges
    def update(self, main):
        if self.spawned:
            if not self.on_ground:
                self.vy += gravity

            blocks = main.get_map().get_blocks_for_collision(self.rect.x // 32, self.rect.y // 32)
            self.move_horizontally(blocks)
            self.move_vertically(blocks)

            self.check_borders(main)
        else:
            self.spawn_animation()

    # Draws the mushroom
    def render(self, main):
        main.screen.blit(self.image, main.get_map().get_camera().apply(self))

# Flower object =====================================================================
class Flower(Entity):
    def __init__(self, x, y):
        super().__init__()

        # Spawning Flags and size
        self.rect = pygame.Rect(x, y, 32, 32)
        self.spawned = False
        self.spawned_y = 0

        # Timer variables for animation
        self.current_image = 0
        self.timer = 0
        self.images = (
            pygame.image.load('images/flower0.png').convert_alpha(),
            pygame.image.load('images/flower1.png').convert_alpha(),
            pygame.image.load('images/flower2.png').convert_alpha(),
            pygame.image.load('images/flower3.png').convert_alpha()
        )

    # Powers up the player when eaten
    def check_collision_with_player(self, main):
        if self.rect.colliderect(main.get_map().get_player().rect):
            main.get_map().get_player().set_size(3, main)
            main.get_map().get_mobs().remove(self)

    # The flower has an idle animation (Flashing)
    def update_image(self):
        self.timer += 1

        if self.timer == 60:
            self.timer = 0
            self.current_image = 0

        elif self.timer % 15 == 0:
            self.current_image += 1

    # The flower spawns up similar to the mushroom
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

# Enemies ======================================================================================================='
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

    # If enemy interacts with the player
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
                        if not main.get_map().get_player().invincible:
                            main.get_map().get_player().Mario_size(0, main)

    # enemies bounce off each other like walls
    def check_collision_with_mobs(self, main):
        for mob in main.get_map().get_mobs():
            if mob is not self:
                if self.rect.colliderect(mob.rect):
                    if mob.collision:
                        mob.die(main, instantly=False, stomped=False)

    # Death animation
    def die(self, main, instantly, stomped):
        if not instantly:
            main.get_map().get_player().add_score(main.get_map().m_points)
            main.get_map().spawn_score_text(self.rect.x + 16, self.rect.y)
            self.state = -1
            self.vy = -4
            self.current_image = 5
        else:
            main.get_map().get_mobs().remove(self)

    # Adds the player a score for defeating them
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

    # Walking animation for the koopa
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

    # Checks for collision and allows them to fall off ledges
    def update(self, main):
        # Walking state
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

        # Shell state
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

    # Draws goomba on the screen 
    def render(self, main):
        main.screen.blit(self.images[self.current_image], main.get_map().get_camera().apply(self))

class Goombas(Entity):
    def __init__(self, x, y, move_direction):
        super().__init__()
        self.rect = pygame.Rect(x, y, 32, 32)

        # Moves enemy left and right
        if move_direction:
            self.vx = 1
        else:
            self.vx = -1
        
        # Flag to check if the enemy was hit
        self.stomped = False

        
        # Animation timers and picture declarations
        self.current_image = 0
        self.frame = 0
        self.images = [
            pygame.image.load('images/goombas_0.png').convert_alpha(),
            pygame.image.load('images/goombas_1.png').convert_alpha(),
            pygame.image.load('images/goombas_dead.png').convert_alpha()
        ]
        self.images.append(pygame.transform.flip(self.images[0], 0, 180))

    # Animations the goomba
    def die(self, main, instantly, stomped):
        if not instantly:
            main.get_map().get_player().add_score(main.get_map().m_points)
            main.get_map().spawn_score_text(self.rect.x + 16, self.rect.y)

            # The enemy squashed animation and removes itself
            if stomped:
                self.stomped = True
                self.frame = 0
                self.current_image = 2
                self.state = -1
                main.get_sound().play('kill_mob', 0, 0.5)
                self.collision = False

            # For interactions with the fireball from the player
            else:
                self.vy = -4
                self.current_image = 3
                main.get_sound().play('shot', 0, 0.5)
                self.state = -1
                self.collision = False
                
        # Removes "dead" enemy from the game
        else:
            main.get_map().get_mobs().remove(self)
    
    # Kills player if the player hits the side of the enemy
    def check_collision_with_player(self, main):
        if self.collision:
            if self.rect.colliderect(main.get_map().get_player().rect):
                if self.state != -1:
                    if main.get_map().get_player().vy > 0:
                        self.die(main, instantly=False, stomped=True)
                        main.get_map().get_player().reset_jump()
                        main.get_map().get_player().jump_on_mob()
                    else:
                        if not main.get_map().get_player().invincible:
                            main.get_map().get_player().set_size(0, main)

    # Idle Animation                       
    def update_image(self):
        self.frame += 1
        if self.frame == 14:
            self.current_image = 1
        elif self.frame == 28:
            self.current_image = 0
            self.frame = 0

    # gives it interactions with map such as falling off and standing on a block
    def update(self, main):
        if self.state == 0:
            self.update_image()

            if not self.on_ground:
                self.vy += gravity

            blocks = main.get_map().get_blocks_for_collision(int(self.rect.x // 32), int(self.rect.y // 32))
            self.move_horizontally(blocks)
            self.move_vertically(blocks)

            self.check_borders(main)
        
        # Getting hit by player
        elif self.state == -1:
            if self.stomped:
                self.frame += 1
                if self.frame == 50:
                    main.get_map().get_mobs().remove(self)
            # Falling down
            else:
                self.vy += gravity
                self.rect.y += self.vy
                self.check_borders(main)

    # Draws enemy on the screen
    def render(self, main):
        main.screen.blit(self.images[self.current_image], main.get_map().get_camera().apply(self))

import pygame
from settings import *


class player(object):
    def __init__(self, x, y):
        self.lives = 3
        self.score = 0
        self.coins = 98
        # The state player is in
        self.size = 0
        self.invincibilityTime = 0
        self.levelUpTime = 0
        self.levelDownTime = 0
        self.spriteTick = 0

        self.visible = True
        self.invincible = False
        self.levelUp = False
        self.levelDown = False
        # Jump variables
        self.mid_jump = False
        self. next_jump_time = 0
        # Fireball variables
        self.fireball_time = 0
        # Movements
        self.vx = 0
        self.vy = 0
        self.direction = True
        self.on_ground = False
        self.moving = False
        # Mario images
        self.image = pygame.image.load('images/mario/mario.png').convert_alpha()
        self.sprites = []
        self.load_sprites()
        # Spawn position
        self.rect = pygame.Rect(x, y, 32, 32)

    def load_sprites(self):
        self.sprites = [
            # 0 Small, stay
            pygame.image.load('images/Mario/mario.png'),

            # 1 Small, move 0
            pygame.image.load('images/Mario/mario_move0.png'),

            # 2 Small, move 1
            pygame.image.load('images/Mario/mario_move1.png'),

            # 3 Small, move 2
            pygame.image.load('images/Mario/mario_move2.png'),

            # 4 Small, jump
            pygame.image.load('images/Mario/mario_jump.png'),

            # 5 Small, end 0
            pygame.image.load('images/Mario/mario_end.png'),

            # 6 Small, end 1
            pygame.image.load('images/Mario/mario_end1.png'),

            # 7 Small, stop
            pygame.image.load('images/Mario/mario_st.png'),

            # =============================================

            # 8 Big, stay
            pygame.image.load('images/Mario/mario1.png'),

            # 9 Big, move 0
            pygame.image.load('images/Mario/mario1_move0.png'),

            # 10 Big, move 1
            pygame.image.load('images/Mario/mario1_move1.png'),

            # 11 Big, move 2
            pygame.image.load('images/Mario/mario1_move2.png'),

            # 12 Big, jump
            pygame.image.load('images/Mario/mario1_jump.png'),

            # 13 Big, end 0
            pygame.image.load('images/Mario/mario1_end.png'),

            # 14 Big, end 1
            pygame.image.load('images/Mario/mario1_end1.png'),

            # 15 Big, stop
            pygame.image.load('images/Mario/mario1_st.png'),

            # =============================================

            # 16 Big_fireball, stay
            pygame.image.load('images/Mario/mario2.png'),

            # 17 Big_fireball, move 0
            pygame.image.load('images/Mario/mario2_move0.png'),

            # 18 Big_fireball, move 1
            pygame.image.load('images/Mario/mario2_move1.png'),

            # 19 Big_fireball, move 2
            pygame.image.load('images/Mario/mario2_move2.png'),

            # 20 Big_fireball, jump
            pygame.image.load('images/Mario/mario2_jump.png'),

            # 21 Big_fireball, end 0
            pygame.image.load('images/Mario/mario2_end.png'),

            # 22 Big_fireball, end 1
            pygame.image.load('images/Mario/mario2_end1.png'),

            # 23 Big_fireball, stop
            pygame.image.load('images/Mario/mario2_st.png'),
        ]

        # Left side
        for i in range(len(self.sprites)):
            self.sprites.append(pygame.transform.flip(self.sprites[i], 180, 0))

        # Power level changing, right
        self.sprites.append(pygame.image.load('images/Mario/mario_lvlup.png').convert_alpha())

        # Power level changing, left
        self.sprites.append(pygame.transform.flip(self.sprites[-1], 180, 0))

        # Death
        self.sprites.append(pygame.image.load('images/Mario/mario_death.png').convert_alpha())

    def update(self, main):
        self.player_physics(main)
        self.update_image(main)
        self.update_invincible_time()

    def player_physics(self, main):
        if main.moveRight:
            # Positive moves to the right
            self.vx += speed_increase
            self.direction = True
        if main.moveLeft:
            # Negative moves to the left
            self.vx -= speed_increase
            self.direction = False
            if self.rect.x <= 0:
                self.vx = 0
                self.rect.x = 0
        if not main.jump_up:
            self.mid_jump = False
        elif main.jump_up:
            if self.on_ground and not self.mid_jump:
                # Moves mario upwards
                self.vy = -jump
                self.mid_jump = True
                self.next_jump_time = pygame.time.get_ticks() + 750
                # If mario is big or fire flower mario
                if self.size >= 1:
                    main.get_sound().play('big_mario_jump', 0, 0.5)
                else:
                    main.get_sound().play('small_mario_jump', 0, 0.5)
        # Fireball shooting and sprinting
        self.sprinting = False
        # if shift is being held down
        if main.shift:
            self.sprinting = True
            if self.size == 2:
                if pygame.time.get_ticks() > self.fireball_time:
                    if not (self.levelUp or self.levelDown):
                        if len(main.get_map().projectiles) < 2:
                            # Shoot the fireball
                            self.shoot(main, self.rect.x, self.rect.y, self.direction)

        if not (main.moveRight or main.moveLeft):
            if self.vx > 0:
                self.vx -= speed_decrease
            elif self.vx < 0:
                self.vx += speed_decrease

        else:
            if self.vx > 0:
                # if it's running, set the movement to max run speed
                if self.sprinting:
                    if self.vx > max_run:
                        self.vx = max_run
                # if it's not running, set movement to max walk
                elif self.vx > max_walk:
                    self.vx = max_walk
            if self.vx < 0:
                # Move to the left
                if self.sprinting:
                    if (-self.vx) > max_run:
                        self.vx = -max_run
                # Move to the left
                else:
                    if (-self.vx) > max_walk:
                        self.vx = -max_walk

        # Computation error
        if 0 < self.vx < speed_decrease:
            self.vx = 0
        if 0 > self.vx > -speed_decrease:
            self.vx = 0

        if not self.on_ground:
            self.vy += gravity
            if self.vy > max_fall:
                self.vy = max_fall

        blocks = main.get_map().get_blocks_for_collision(self.rect.x // 32, self.rect.y // 32)

        if self.vx > 0:
            self.rect.x += (self.vx + 1)
        else:
            self.rect.x += self.vx
        self.update_x_pos(blocks)

        self.rect.y += self.vy
        self.update_y_pos(blocks, main)

        # on_ground needs this piece of code
        coord_y = self.rect.y // 32
        if self.size > 0:
            coord_y += 1
        for block in main.get_map().get_blocks_below(self.rect.x // 32, coord_y):
            if block != 0 and block.type != 'BGObject':
                if pygame.Rect(self.rect.x, self.rect.y + 1, self.rect.width, self.rect.height).colliderect(block.rect):
                    self.on_ground = True

        # Map border check
        if self.rect.y > 448:
            main.get_map().player_death(main)

        # End Flag collision check
        if self.rect.colliderect(main.get_map().flag.pole_rect):
            main.get_map().player_win(main)

    def set_image(self, new_image):

        # "Dead" sprite
        if new_image == len(self.sprites):
            self.image = self.sprites[-1]

        elif self.direction:
            self.image = self.sprites[new_image + self.size * 8]
        else:
            self.image = self.sprites[new_image + self.size * 8 + 24]

    def update_image(self, main):

        self.spriteTick += 1

        if self.size in (0, 1, 2):

            if self.vx == 0:
                self.set_image(0)
                self.spriteTick = 0

            # Player is running
            elif (
                    ((self.vx > 0 and main.moveRight and not main.moveLeft) or
                     (self.vx < 0 and main.moveLeft and not main.moveRight)) or
                    (self.vx > 0 and not (main.moveLeft or main.moveRight)) or
                    (self.vx < 0 and not (main.moveLeft or main.moveRight))
            ):
                if self.spriteTick <= 10:
                    self.set_image(1)
                elif 11 <= self.spriteTick <= 20:
                    self.set_image(2)
                elif 21 <= self.spriteTick <= 30:
                    self.set_image(3)
                elif self.spriteTick == 31:
                    self.spriteTick = 0
                    self.set_image(1)

            # When the player still has acceleration but moves to the opposite direction
            elif (self.vx > 0 and main.moveLeft and not main.moveRight) or (self.vx < 0 and main.moveRight and not main.moveLeft):
                self.set_image(7)
                self.spriteTick = 0

            if not self.on_ground:
                self.spriteTick = 0
                self.set_image(4)

    # Function for the invincibility time when mario gets hit
    def update_invincible_time(self):
        if self.invincible:
            self.invincibilityTime -= 1
            if self.invincibilityTime == 0:
                self.invincible = False

    def update_x_pos(self, blocks):
        for block in blocks:
            if block != 0 and block.type != 'BGObject':
                block.debugLight = True
                if pygame.Rect.colliderect(self.rect, block.rect):
                    if self.vx > 0:
                        self.rect.right = block.rect.left
                        self.vx = 0
                    elif self.vx < 0:
                        self.rect.left = block.rect.right
                        self.vx = 0

    def update_y_pos(self, blocks, main):
        self.on_ground = False
        for block in blocks:
            if block != 0 and block.type != 'BGObject':
                if pygame.Rect.colliderect(self.rect, block.rect):

                    if self.vy > 0:
                        self.on_ground = True
                        self.rect.bottom = block.rect.top
                        self.vy = 0

                    elif self.vy < 0:
                        self.rect.top = block.rect.bottom
                        self.vy = -self.vy / 3
                        self.block_movement(main, block)

    # Function for when a block gets hit
    def block_movement(self, main, block):
        # Question Block
        if block.typeID == 22:
            main.get_sound().play('block_hit', 0, 0.5)
            if not block.isActivated:
                block.spawn_bonus(main)

        # Brick Platform
        elif block.typeID == 23:
            if self.size == 0:
                block.shaking = True
                main.get_sound().play('block_hit', 0, 0.5)
            else:
                block.destroy(main)
                main.get_sound().play('brick_break', 0, 0.5)
                self.add_score(50)

    def reset(self, reset_all):
        self.direction = True
        self.rect.x = 96
        self.rect.y = 351
        if self.size != 0:
            self.size = 0
            self.rect.y += 32
            self.rect.height = 32

        if reset_all:
            self.score = 0
            self.coins = 98
            self.lives = 3

            self.visible = True
            self.spriteTick = 0
            self.size = 0
            self.levelUp = False
            self.levelUpTime = 0

            self.invincible = False
            self.invincibilityTime = 0

            self.levelDown = False
            self.levelDownTime = 0

            self.mid_jump = False
            self.vx = 0
            self.vy = 0
            self.on_ground = False

    def reset_jump(self):
        self.vy = 0
        self.mid_jump = False

    def reset_move(self):
        self.vx = 0
        self.vy = 0

    # If player jumps on a mob
    def jump_on_mob(self):
        self.mid_jump = True
        self.vy = -4
        self.rect.y -= 6

    def set_size(self, mario_state, main):
        if self.size == 0 == mario_state and not self.invincible:
            main.get_map().player_death(main)
            self.levelUp = False
            self.levelDown = False

        elif self.size == 0 and self.size < mario_state:
            self.size = 1
            main.get_sound().play('mushroom_eat', 0, 0.5)
            main.get_map().spawn_score_text(self.rect.x + 16, self.rect.y, score=1000)
            self.add_score(1000)
            self.levelUp = True
            self.levelUpTime = 61

        elif self.size == 1 and self.size < mario_state:
            main.get_sound().play('mushroom_eat', 0, 0.5)
            main.get_map().spawn_score_text(self.rect.x + 16, self.rect.y, score=1000)
            self.add_score(1000)
            self.size = 2

        elif self.size > mario_state:
            main.get_sound().play('pipe', 0, 0.5)
            self.levelDown = True
            self.levelDownTime = 200
            self.invincible = True
            self.invincibilityTime = 200

        else:
            main.get_sound().play('mushroom_eat', 0, 0.5)
            main.get_map().spawn_score_text(self.rect.x + 16, self.rect.y, score=1000)
            self.add_score(1000)

    # The transition between small and big player
    def change_animation(self):

        if self.levelDown:
            self.levelDownTime -= 1

            if self.levelDownTime == 0:
                self.levelDown = False
                self.visible = True
            elif self.levelDownTime % 20 == 0:
                if self.visible:
                    self.visible = False
                else:
                    self.visible = True
                if self.levelDownTime == 100:
                    self.size = 0
                    self.rect.y += 32
                    self.rect.height = 32

        elif self.levelUp:
            self.levelUpTime -= 1

            if self.levelUpTime == 0:
                self.levelUp = False
                self.rect.y -= 32
                self.rect.height = 64

            elif self.levelUpTime in (60, 30):
                self.image = self.sprites[-3] if self.direction else self.sprites[-2]
                self.rect.y -= 16
                self.rect.height = 48

            elif self.levelUpTime in (45, 15):
                self.image = self.sprites[0] if self.direction else self.sprites[24]
                self.rect.y += 16
                self.rect.height = 32

    def flag_animation_move(self, main, walk_to_castle):
        if walk_to_castle:
            self.direction = True

            if not self.on_ground:
                self.vy += gravity if self.vy <= max_fall else 0

            x = self.rect.x // 32
            y = self.rect.y // 32
            blocks = main.get_map().get_blocks_for_collision(x, y)

            self.rect.x += self.vx
            if self.rect.colliderect(main.get_map().map[205][11]):
                self.visible = False
                main.get_map().get_event().player_in_castle = True
            self.update_x_pos(blocks)

            self.rect.top += self.vy
            self.update_y_pos(blocks, main)

            # on_ground works incorrect without this piece of code
            x = self.rect.x // 32
            y = self.rect.y // 32
            if self.size > 0:
                y += 1
            for block in main.get_map().get_blocks_below(x, y):
                if block != 0 and block.type != 'BGObject':
                    if pygame.Rect(self.rect.x, self.rect.y + 1, self.rect.width, self.rect.height).colliderect(block.rect):
                        self.on_ground = True

        else:
            if main.get_map().flag.flag_rect.y + 20 > self.rect.y + self.rect.height:
                self.rect.y += 3

    def shoot(self, main, x, y, orientation):
        main.get_map().spawn_fireball(x, y, orientation)
        main.get_sound().play('fireball', 0, 0.5)
        self.fireball_time = pygame.time.get_ticks() + 400

    def add_coins(self, count):
        self.coins += count
        if self.coins >= 100:
            self.coins = 0
            self.lives += 1

    def add_score(self, count):
        self.score += count

    def render(self, main):
        if self.visible:
            main.screen.blit(self.image, main.get_map().get_camera().apply(self))

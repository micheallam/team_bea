import pygame
from pytmx.util_pygame import load_pygame
from game_ui import game_ui
from bgobject import BGObject
from camera import Camera
from event import Event
from flag import Flag
from settings import *
from Platform import Platform
from player import player

# Entity imports
from entity import Goombas
from entity import Mushroom
from entity import Flower
from entity import Koopa

# Misc imports
from Tube import Tube
from PlatformDebris import PlatformDebris
from CoinHit import CoinHit
from fireball import Fireball
from text import text

# Creates the map and initializes several lists
class Map(object):
    def __init__(self, world_num):
        self.obj = []
        self.obj_bg = []
        self.tubes = []
        self.debris = []
        self.mobs = []
        self.projectiles = []
        self.text_objects = []
        self.map = 0
        self.flag = None

        self.map_size = (0, 0)
        self.sky = 0

        self.textures = {}
        self.world_num = world_num
        self.load_world_11()

        # enemies spawn when the player is a set distance from them
        self.is_mob_spawned = [False, False, False, False]
        self.m_points = 100
        self.score_time = 0

        self.in_event = False
        self.tick = 0
        self.time = 400

        # General camera settings
        self.object_player = player(x=128, y=351)
        self.object_camera = Camera(self.map_size[0] * 32, 14)
        self.object_event = Event()
        self.object_game_ui = game_ui()

# uses a file to load in pre determined locations of the world via text file        
    def load_world_11(self):
        data = load_pygame("worlds/1-1/W11.tmx")
        self.map_size = (data.width, data.height)

        self.sky = pygame.Surface((screen_width, screen_height))
        self.sky.fill((92, 148, 252))

        self.map = [[0] * data.height for i in range(data.width)]

        # Sets the different layers so mario does not interact with all items on the screen
        layer_num = 0
        for layer in data.visible_layers:
            for y in range(data.height):
                for x in range(data.width):

                    image = data.get_tile_image(x, y, layer_num)

                    if image is not None:
                        tile_id = data.get_tile_gid(x, y, layer_num)

                        if layer.name == 'Foreground':

                            if tile_id == 22:
                                image = (
                                    image,  # 1
                                    data.get_tile_image(0, 15, layer_num),  # 2
                                    data.get_tile_image(1, 15, layer_num),  # 3
                                    data.get_tile_image(2, 15, layer_num)  # activated
                                )

                            self.map[x][y] = Platform(x * data.tileheight, y * data.tilewidth, image, tile_id)
                            self.obj.append(self.map[x][y])

                        elif layer.name == 'Background':
                            self.map[x][y] = BGObject(x * data.tileheight, y * data.tilewidth, image)
                            self.obj_bg.append(self.map[x][y])
            layer_num += 1

# Specific positons of the world object ======================================================================
        self.spawn_tube(28, 10)
        self.spawn_tube(37, 9)
        self.spawn_tube(46, 8)
        self.spawn_tube(55, 8)
        self.spawn_tube(163, 10)
        self.spawn_tube(179, 10)

        # Mobs
        self.mobs.append(Goombas(736, 352, False))
        self.mobs.append(Goombas(1295, 352, True))
        self.mobs.append(Goombas(1632, 352, False))
        self.mobs.append(Goombas(1672, 352, False))
        self.mobs.append(Goombas(5570, 352, False))
        self.mobs.append(Goombas(5620, 352, False))

        self.map[21][8].bonus = 'mushroom'
        self.map[78][8].bonus = 'mushroom'
        self.map[109][4].bonus = 'mushroom'

        self.flag = Flag(6336, 48)

# upon death, the game reinitializes all objects ======================================================================        
    def reset(self, reset_all):
        self.obj = []
        self.obj_bg = []
        self.tubes = []
        self.debris = []
        self.mobs = []
        self.is_mob_spawned = [False, False, False, False]

        self.in_event = False
        self.flag = None
        self.sky = None
        self.map = None

        self.tick = 0
        self.time = 400

        self.map_size = (0, 0)
        self.textures = {}
        self.load_world_11()

        self.get_event().reset()
        self.get_player().reset(reset_all)
        self.get_camera().reset()

# Returns the UI information ============================================================================================        
    def get_name(self):
        if self.world_num == '1-1':
            return '1-1'

    def get_player(self):
        return self.object_player

    def get_camera(self):
        return self.object_camera

    def get_event(self):
        return self.object_event

    def get_ui(self):
        return self.object_game_ui

# Collides with the sides and top of a block ======================================================================    
    def get_blocks_for_collision(self, x, y):
        return (
            self.map[x][y - 1],
            self.map[x][y + 1],
            self.map[x][y],
            self.map[x - 1][y],
            self.map[x + 1][y],
            self.map[x + 2][y],
            self.map[x + 1][y - 1],
            self.map[x + 1][y + 1],
            self.map[x][y + 2],
            self.map[x + 1][y + 2],
            self.map[x - 1][y + 1],
            self.map[x + 2][y + 1],
            self.map[x][y + 3],
            self.map[x + 1][y + 3]
        )
# Collides with the bottom of the block ======================================================================
    def get_blocks_below(self, x, y):
        return (
            self.map[x][y + 1],
            self.map[x + 1][y + 1]
        )
    
# Several spawn declarations of various objects ======================================================================
    def get_mobs(self):
        return self.mobs

    def spawn_tube(self, x_coord, y_coord):
        self.tubes.append(Tube(x_coord, y_coord))

        for y in range(y_coord, 12):  # 12 because it's ground level.
            for x in range(x_coord, x_coord + 2):
                self.map[x][y] = Platform(x * 32, y * 32, image=None, type_id=0)

    def spawn_mushroom(self, x, y):
        self.get_mobs().append(Mushroom(x, y, True))

    def spawn_goombas(self, x, y, move_direction):
        self.get_mobs().append(Goombas(x, y, move_direction))

    def spawn_koopa(self, x, y, move_direction):
        self.get_mobs().append(Koopa(x, y, move_direction))

    def spawn_flower(self, x, y):
        self.mobs.append(Flower(x, y))

    def spawn_debris(self, x, y, type):
        if type == 0:
            self.debris.append(PlatformDebris(x, y))
        elif type == 1:
            self.debris.append(CoinHit(x, y))

    def spawn_fireball(self, x, y, move_direction):
        self.projectiles.append(Fireball(x, y, move_direction))

    def spawn_score_text(self, x, y, score=None):
        if score is None:
            self.text_objects.append(text(str(self.m_points), 16, (x, y)))
            self.score_time = pygame.time.get_ticks()
            if self.m_points < 1600:
                self.m_points *= 2
        else:
            self.text_objects.append(text(str(score), 16, (x, y)))

# Various removal of object definitions ======================================================================            
    def remove_object(self, object):
        self.obj.remove(object)
        self.map[object.rect.x // 32][object.rect.y // 32] = 0

    def remove_whizbang(self, whizbang):
        self.projectiles.remove(whizbang)

    def remove_text(self, text_object):
        self.text_objects.remove(text_object)

# Various Update defitinitions ====================================================================================   
    def update_player(self, main):
        self.get_player().update(main)

    def update_entities(self, main):
        for mob in self.mobs:
            mob.update(main)
            if not self.in_event:
                self.entity_collisions(main)

    def update_time(self, main):
        if not self.in_event:
            self.tick += 1
            if self.tick % 40 == 0:
                self.time -= 1
                self.tick = 0
            if self.time == 100 and self.tick == 1:
                main.get_sound().start_fast_music(main)
            elif self.time == 0:
                self.player_death(main)

    def update_score_time(self):
        if self.m_points != 100:
            if pygame.time.get_ticks() > self.score_time + 750:
                self.m_points //= 2

    def entity_collisions(self, main):
        if not main.get_map().get_player().invincible:
            for mob in self.mobs:
                mob.check_collision_with_player(main)

    def try_spawn_mobs(self, main):
        if self.get_player().rect.x > 2080 and not self.is_mob_spawned[0]:
            self.spawn_goombas(2495, 224, False)
            self.spawn_goombas(2560, 96, False)
            self.is_mob_spawned[0] = True

        elif self.get_player().rect.x > 2700 and not self.is_mob_spawned[1]:
            self.spawn_goombas(3200, 352, False)
            self.spawn_goombas(3250, 352, False)
            self.spawn_koopa(3400, 352, False)
            self.is_mob_spawned[1] = True	
            
        elif self.get_player().rect.x > 3300 and not self.is_mob_spawned[2]:
            self.spawn_goombas(3700, 352, False)
            self.spawn_goombas(3750, 352, False)
            self.is_mob_spawned[2] = True
            
        elif self.get_player().rect.x > 3600 and not self.is_mob_spawned[3]:
            self.spawn_goombas(4060, 352, False)
            self.spawn_goombas(4110, 352, False)
            self.spawn_goombas(4190, 352, False)
            self.spawn_goombas(4240, 352, False)
            self.is_mob_spawned[3] = True

    # when the player dies the values are all updated accordingly       
    def player_death(self, main):
        self.in_event = True
        self.get_player().reset_jump()
        self.get_player().reset_move()
        self.get_player().lives -= 1

        if self.get_player().lives == 0:
            self.get_event().start_death(main, game_over=True)
        else:
            self.get_event().start_death(main, game_over=False)
    
    # Starts the win animation at the end of the level
    def player_win(self, main):
        self.in_event = True
        self.get_player().reset_jump()
        self.get_player().reset_move()
        self.get_event().start_win(main)

    # updates the world and handles flags for animations ==================================================================
    def update(self, main):
        self.update_entities(main)
        if not main.get_map().in_event:
            if self.get_player().levelUp:
                self.get_player().change_animation()
            elif self.get_player().levelDown:
                self.get_player().change_animation()
                self.update_player(main)
            else:
                self.update_player(main)
        else:
            self.get_event().update(main)
        for debris in self.debris:
            debris.update(main)
        for whizbang in self.projectiles:
            whizbang.update(main)
        for text_object in self.text_objects:
            text_object.update(main)
        if not self.in_event:
            self.get_camera().update(main.get_map().get_player().rect)
        self.try_spawn_mobs(main)
        self.update_time(main)
        self.update_score_time()

    def render_map(self, main):
        main.screen.blit(self.sky, (0, 0))
        for obj_group in (self.obj_bg, self.obj):
            for obj in obj_group:
                obj.render(main)
        for tube in self.tubes:
            tube.render(main)

    # Draws all objects into the game =====================================================================================================        
    def render(self, main):

        main.screen.blit(self.sky, (0, 0))

        for obj in self.obj_bg:
            obj.render(main)

        for mob in self.mobs:
            mob.render(main)

        for obj in self.obj:
            obj.render(main)

        for tube in self.tubes:
            tube.render(main)

        for whizbang in self.projectiles:
            whizbang.render(main)

        for debris in self.debris:
            debris.render(main)

        self.flag.render(main)

        for text_object in self.text_objects:
            text_object.render_in_game(main)

        self.get_player().render(main)

        self.get_ui().render(main)

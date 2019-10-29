import pygame
from pytmx.util_pygame import load_pygame

from game_ui import game_ui
from bg_object import bg_object
from camera import camera
from event import event
from flag import flag
from settings import *
from platform import platform
from player import player
from goombas import goombas
from mushroom import mushroom
from flower import flower
from koopa import koopa
from tube import tube
from platform_debris import platform_debris
from coin_debris import coin_debris
from fireball import fireball
from text import text


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

        self.is_mob_spawned = [False, False]
        self.m_points = 100
        self.score_time = 0

        self.in_event = False
        self.tick = 0
        self.time = 400

        self.object_player = player(x_pos=128, y_pos=351)
        self.object_camera = camera(self.map_size[0] * 32, 14)
        self.object_event = event()
        self.object_game_ui = game_ui()

    def load_world_11(self):
        data = load_pygame("worlds/1-1/W11.txt")
        self.map_size = (data.width, data.height)

        self.sky = pygame.Surface((WINDOW_W, WINDOW_H))
        self.sky.fill((pygame.Color((92, 148, 252))))

        self.map = [[0] * data.height for i in range(data.width)]

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
                                    image,                                   # 1
                                    data.get_tile_image(0, 15, layer_num),   # 2
                                    data.get_tile_image(1, 15, layer_num),   # 3
                                    data.get_tile_image(2, 15, layer_num)    # activated
                                )

                            self.map[x][y] = platform(x * data.tile_height, y * data.tile_width, image, tile_id)
                            self.obj.append(self.map[x][y])

                        elif layer.name == 'Background':
                            self.map[x][y] = bg_object(x * data.tile_height, y * data.tile_width, image)
                            self.obj_bg.append(self.map[x][y])
            layer_num += 1

        # tubes
        self.spawn_tube(28, 10)
        self.spawn_tube(37, 9)
        self.spawn_tube(46, 8)
        self.spawn_tube(55, 8)
        self.spawn_tube(163, 10)
        self.spawn_tube(179, 10)

        # Mobs
        self.mobs.append(goombas(736, 352, False))
        self.mobs.append(goombas(1295, 352, True))
        self.mobs.append(goombas(1632, 352, False))
        self.mobs.append(goombas(1672, 352, False))
        self.mobs.append(goombas(5570, 352, False))
        self.mobs.append(goombas(5620, 352, False))

        self.map[21][8].bonus = 'mushroom'
        self.map[78][8].bonus = 'mushroom'
        self.map[109][4].bonus = 'mushroom'

        self.flag = flag(6336, 48)

    def reset(self, reset_all):
        self.obj = []
        self.obj_bg = []
        self.tubes = []
        self.debris = []
        self.mobs = []

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

    def get_blocks_below(self, x, y):
        return (
            self.map[x][y + 1],
            self.map[x + 1][y + 1]
        )

    def get_mobs(self):
        return self.mobs

    def spawn_tube(self, x_coord, y_coord):
        self.tubes.append(tube(x_coord, y_coord))

        for y in range(y_coord, 12): # 12 because it's ground level.
            for x in range(x_coord, x_coord + 2):
                self.map[x][y] = platform(x * 32, y * 32, image=None, type_id=0)

    def spawn_mushroom(self, x, y):
        self.get_mobs().append(mushroom(x, y, True))

    def spawn_goombas(self, x, y, move_direction):
        self.get_mobs().append(goombas(x, y, move_direction))

    def spawn_koopa(self, x, y, move_direction):
        self.get_mobs().append(koopa(x, y, move_direction))

    def spawn_flower(self, x, y):
        self.mobs.append(flower(x, y))

    def spawn_debris(self, x, y, type):
        if type == 0:
            self.debris.append(platform_debris(x, y))
        elif type == 1:
            self.debris.append(coin_debris(x, y))

    def spawn_fireball(self, x, y, move_direction):
        self.projectiles.append(fireball(x, y, move_direction))

    def spawn_score_text(self, x, y, score=None):
        if score is None:
            self.text_objects.append(text(str(self.m_points), 16, (x, y)))
            self.score_time = pygame.time.get_ticks()
            if self.m_points < 1600:
                self.m_points *= 2
        else:
            self.text_objects.append(text(str(score), 16, (x, y)))

    def remove_object(self, object):
        self.obj.remove(object)
        self.map[object.rect.x // 32][object.rect.y // 32] = 0

    def remove_shoot(self, shoot):
        self.projectiles.remove(shoot)

    def remove_text(self, text_object):
        self.text_objects.remove(text_object)

    def update_player(self, core):
        self.get_player().update(core)

    def update_entities(self, core):
        for mob in self.mobs:
            mob.update(core)
            if not self.in_event:
                self.entity_collisions(core)

    def update_time(self, core):
        if not self.in_event:
            self.tick += 1
            if self.tick % 40 == 0:
                self.time -= 1
                self.tick = 0
            if self.time == 100 and self.tick == 1:
                core.get_sound().start_fast_music(core)
            elif self.time == 0:
                self.player_death(core)

    def update_score_time(self):
        if self.m_points != 100:
            if pygame.time.get_ticks() > self.score_time + 750:
                self.m_points //= 2
    def entity_collisions(self, core):
        if not core.get_map().get_player().unkillable:
            for mob in self.mobs:
                mob.check_collision_with_player(core)
    def try_spawn_mobs(self, core):
        if self.get_player().rect.x > 2080 and not self.is_mob_spawned[0]:
            self.spawn_goombas(2495, 224, False)
            self.spawn_goombas(2560, 96, False)
            self.is_mob_spawned[0] = True

        elif self.get_player().rect.x > 2460 and not self.is_mob_spawned[1]:
            self.spawn_goombas(3200, 352, False)
            self.spawn_goombas(3250, 352, False)
            self.spawn_koopa(3400, 352, False)
            self.spawn_goombas(3700, 352, False)
            self.spawn_goombas(3750, 352, False)
            self.spawn_goombas(4060, 352, False)
            self.spawn_goombas(4110, 352, False)
            self.spawn_goombas(4190, 352, False)
            self.spawn_goombas(4240, 352, False)
            self.is_mob_spawned[1] = True

    def player_death(self, core):
        self.in_event = True
        self.get_player().reset_jump()
        self.get_player().reset_move()
        self.get_player().numOfLives -= 1

        if self.get_player().numOfLives == 0:
            self.get_event().start_kill(core, game_over=True)
        else:
            self.get_event().start_kill(core, game_over=False)

    def player_win(self, core):
        self.in_event = True
        self.get_player().reset_jump()
        self.get_player().reset_move()
        self.get_event().start_win(core)

    def update(self, core):
        self.update_entities(core)
        if not core.get_map().in_event:
            if self.get_player().inLevelUpAnimation:
                self.get_player().change_powerlvl_animation()
            elif self.get_player().inLevelDownAnimation:
                self.get_player().change_powerlvl_animation()
                self.update_player(core)
            else:
                self.update_player(core)
        else:
            self.get_event().update(core)
        for debris in self.debris:
            debris.update(core)
        for shoot in self.projectiles:
            shoot.update(core)
        for text_object in self.text_objects:
            text_object.update(core)
        if not self.in_event:
            self.get_camera().update(core.get_map().get_player().rect)
        self.try_spawn_mobs(core)
        self.update_time(core)
        self.update_score_time()
    def render_map(self, core):
        core.screen.blit(self.sky, (0, 0))
        for obj_group in (self.obj_bg, self.obj):
            for obj in obj_group:
                obj.render(core)
        for tube in self.tubes:
            tube.render(core)
    def render(self, core):
	
        core.screen.blit(self.sky, (0, 0))

        for obj in self.obj_bg:
            obj.render(core)

        for mob in self.mobs:
            mob.render(core)

        for obj in self.obj:
            obj.render(core)

        for tube in self.tubes:
            tube.render(core)

        for shoot in self.projectiles:
            shoot.render(core)

        for debris in self.debris:
            debris.render(core)

        self.flag.render(core)

        for text_object in self.text_objects:
            text_object.render_in_game(core)

        self.get_player().render(core)

        self.get_ui().render(core)
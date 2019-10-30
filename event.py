import pygame

from settings import *


class Event(object):
    def __init__(self):
        self.type = 0

        self.delay = 0
        self.time = 0
        self.vx = 0
        self.vy = 0
        self.game_over = False

        self.player_in_castle = False
        self.tick = 0
        self.score_tick = 0

    def reset(self):
        self.type = 0

        self.delay = 0
        self.time = 0
        self.vx = 0
        self.vy = 0
        self.game_over = False

        self.player_in_castle = False
        self.tick = 0
        self.score_tick = 0

    def start_death(self, main, game_over):
        self.type = 0
        self.delay = 4000
        self.vy = -4
        self.time = pygame.time.get_ticks()
        self.game_over = game_over

        main.get_sound().stop('overworld')
        main.get_sound().stop('overworld_fast')
        main.get_sound().play('death', 0, 0.5)

        main.get_map().get_player().set_image(len(main.get_map().get_player().sprites))

    def start_win(self, main):
        self.type = 1
        self.delay = 2000
        self.time = 0

        main.get_sound().stop('overworld')
        main.get_sound().stop('overworld_fast')
        main.get_sound().play('level_end', 0, 0.5)

        main.get_map().get_player().set_image(5)
        main.get_map().get_player().vx = 1
        main.get_map().get_player().rect.x += 10

        if main.get_map().time >= 300:
            main.get_map().get_player().add_score(5000)
            main.get_map().spawn_score_text(main.get_map().get_player().rect.x + 16, main.get_map().get_player().rect.y, score=5000)
        elif 200 <= main.get_map().time < 300:
            main.get_map().get_player().add_score(2000)
            main.get_map().spawn_score_text(main.get_map().get_player().rect.x + 16, main.get_map().get_player().rect.y, score=2000)
        else:
            main.get_map().get_player().add_score(1000)
            main.get_map().spawn_score_text(main.get_map().get_player().rect.x + 16, main.get_map().get_player().rect.y, score=1000)

    def update(self, main):
        if self.type == 0:
            self.vy += gravity if self.vy < 6 else 6
            main.get_map().get_player().rect.y += self.vy

            if pygame.time.get_ticks() > self.time + self.delay:
                if not self.game_over:
                    main.get_map().get_player().reset_move()
                    main.get_map().get_player().reset_jump()
                    main.get_map().reset(False)
                    main.get_sound().play('overworld', 9999999, 0.5)
                else:
                    main.get_mm().current_state = 'Loading'
                    main.get_mm().object_loading_menu.set_text_type('GAME OVER', False)
                    main.get_mm().object_loading_menu.update_time()
                    main.get_sound().play('game_over', 0, 0.5)

        elif self.type == 1:
            if not self.player_in_castle:
                if not main.get_map().flag.flag_spawn:
                    main.get_map().get_player().set_image(5)
                    main.get_map().flag.move_flag_down()
                    main.get_map().get_player().flag_animation_move(main, False)
                else:
                    self.tick += 1
                    if self.tick == 1:
                        main.get_map().get_player().direction = False
                        main.get_map().get_player().set_image(6)
                        main.get_map().get_player().rect.x += 20
                    elif self.tick >= 30:
                        main.get_map().get_player().flag_animation_move(main, True)
                        main.get_map().get_player().update_image(main)
            else:
                if main.get_map().time > 0:
                    self.score_tick += 1
                    if self.score_tick % 10 == 0:
                        main.get_sound().play('scorering', 0, 0.5)
                    main.get_map().time -= 1
                    main.get_map().get_player().add_score(50)
                else:
                    if self.time == 0:
                        self.time = pygame.time.get_ticks()
                    elif pygame.time.get_ticks() >= self.time + self.delay:
                        main.get_mm().current_state = 'Loading'
                        main.get_mm().object_loading_menu.set_text_type('1-2 DLC $4.99: Available in E-Shop.', False)
                        main.get_mm().object_loading_menu.update_time()
                        main.get_sound().play('game_over', 0, 0.5)


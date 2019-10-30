import pygame

from settings import *
from text import text

# Screen after the player presses enter to play
class loading_menu(object):
    def __init__(self, main):
        self.now = pygame.time.get_ticks()
        self.loading_type = True
        self.bg = pygame.Surface((screen_width, screen_height))
        self.text = text('World ' + main.object_world.get_name(), 52, (screen_width / 2, screen_height / 2))
    
    # Plays the game music
    def update(self, main):
        if pygame.time.get_ticks() >= self.now + (5250 if not self.loading_type else 2500):
            if self.loading_type:
                main.object_menu_manager.current_state = 'Game'
                main.get_sound().play('overworld', -1, 0)
                main.get_map().in_event = False
            else:
                main.object_menu_manager.current_state = 'MainMenu'
                self.set_text_type('WORLD ' + main.object_world.get_name(), True)
                main.get_map().reset(True)

    # Centers text on the screen
    def set_text_type(self, message, type):
        self.text = text(message, 32, (screen_width / 2, screen_height / 2))
        self.loading_type = type

    def render(self, main):
        main.screen.blit(self.bg, (0, 0))
        self.text.render(main)
    
    def update_time(self):
        self.now = pygame.time.get_ticks()

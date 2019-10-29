import pygame

from settings import *
from text import text

class loading_menu(object):
    def __init__(self, main):
        self.now = pg.time.get_ticks()
        self.loading_type = True
        self.bg = pg.Surface((screen_width, screen_height))
        self.text = Text('World ' + main.object_world.get_name(), 32, (screen_height / 2, screen_width / 2))
        
    def update(self, main):
        if self.loading_type:
            main.object_menu_manager.current_state = 'Game'
            main.get_sound().play('overworld', -1, 0)
            main.get_map().in_event = False
        else:
            main.object_menu_manager.current_state = 'MainMenu'
            self.set_text_type('WORLD ' + main.object_world.get_name(), True)
            main.get_map().reset(True)
            
    def set_text_type(self, text, type):
        self.text = Text(text, 32, (screen_width / 2, screen_height / 2))
        self.loading_type = type
        
    def render(self, main):
        main.screen.blit(self.bg, (0,0))
        self.text.render(main)
        
    def update_time(self):
        self.now = pg.time.get_ticcks()
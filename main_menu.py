import pygame

from settings import *
from text import text

class main_menu(object):
    def __init__(self):
        self.main_image = pg.image.load('images\title.png').convert_alpha()
        
        self.start_text = Text('Press ENTER to start', 16, (screen_width/2, window_height * .7))
        
    def render(self, main):
        core.screen.blit(self.main_image, (224, 50))
        self.start_text.render(main)
import pygame

from settings import *
from text import text

class main_menu(object):
    def __init__(self):
        self.main_image = pygame.image.load('images/title.png').convert_alpha()
        
        self.start_text = text('Press ENTER to start', 52, (screen_width/2, screen_height * .7))
        
    def render(self, main):
        main.screen.blit(self.main_image, (224, 50))
        self.start_text.render(main)
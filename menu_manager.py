import pygame

from loading_menu import loading_menu
from main_menu import main_menu


class menu_manager(object):
    def __init__(self, main):
        self.current_state = 'MainMenu'
        
        self.object_main_menu = main_menu()
        self.object_loading_menu = loading_menu(main)
        
    def update(self, main):
        if self.current_state == 'MainMenu':
            pass
        elif self.current_state == 'Loading':
            self.object_loading_menu.update(main)
        elif self.current_state == 'Game':
            main.get_map().update(main)
            
    def render(self, main):
        if self.current_state == 'MainMenu':
            main.get_map().render_map(main)
            self.object_main_menu.render(main)
        elif self.current_state == 'Loading':
            self.object_loading_menu.render(main)
        elif self.current_state == 'Game':
            main.get_map().render(main)
            main.get_map().get_ui().render(main)
        
        pygame.display.update()
        
    def start_loading(self):
        self.current_state = 'Loading'
        self.object_loading_menu.update_time()
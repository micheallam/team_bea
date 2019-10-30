from os import environ
import pygame
from pygame.locals import *
from settings import *
from map import Map
from menu_manager import menu_manager
from Sound import Sound


class Main(object):
    def __init__ (self):
        environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.mixer.pre_init(44100, -16, 2, 1024)
        pygame.init()
        pygame.display.set_caption('Team Bea Mario')
        pygame.display.set_mode((screen_width, screen_height))

        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()

        self.object_world = Map('1-1')
        self.object_sound = Sound()
        self.object_menu_manager = menu_manager(self)

        self.run = True # Flag for starting the game
        self.moveRight = False
        self.moveLeft = False
        self.jump_up = False
        self.crouch = False # Goes into pipes or crouches
        self.shift = False # Runs when shift is held down

    def run_game(self):
        while self.run:
            self.input()
            self.update()
            self.render()
            self.clock.tick(fps)

    def input(self):
        if self.get_mm().current_state == 'Game':
            # Places the player in the game
            self.make_player()
        else:
            # Makes the menu if the game isnt running
            self.create_menu()

    def make_player(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            # If these keys are pressed down
            elif event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    self.moveRight = True
                elif event.key == K_LEFT:
                    self.moveLeft = True
                elif event.key == K_UP or event.key == K_SPACE:
                    self.jump_up = True
                elif event.key == K_LSHIFT:
                    self.shift = True

            # If these keys are let go
            elif event.type == KEYUP:
                if event.key == K_RIGHT:
                    self.moveRight = False
                if event.key == K_LEFT:
                    self.moveLeft = False
                if event.key == K_UP or event.key == K_SPACE:
                    self.jump_up = False
                if event.key == K_LSHIFT:
                    self.shift = False

    def create_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    self.get_mm().start_loading()

    def update(self):
        self.get_mm().update(self)

    def render(self):
        self.get_mm().render(self)

    def get_map(self):
        return self.object_world

    def get_mm(self):
        return self.object_menu_manager

    def get_sound(self):
        return self.object_sound

# Runs the game
objectMain = Main()
objectMain.run_game()

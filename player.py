import pygame
from settings import *

class player(object):
    def __init__(self, x, y):
        self.lives = 3
        self.score = 0
        self.coins = 0
        # The state player is in
        self.size = 0
        self.invincibilityTime = 0
        self.levelUp = 0
        self.levelDown = 0

        self.visible = True
        self.invincible = False
        self.levelUp = False
        self.levelDown = False



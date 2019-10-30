import pygame
from settings import *


class Camera(object):
    # Controls the camera moving left and right
    def __init__(self, screen_width, screen_height):
        self.rect = pygame.Rect(0, 0, screen_width, screen_height)
        self.camera(self.rect)

    def camera(self, screen_rect):
        x, y = screen_rect.x, screen_rect.y
        y = screen_rect.y
        width, height = self.rect.width, self.rect.height
        x, y = (-x + screen_width / 2 - screen_rect.width / 2), (-y + screen_height / 2 - screen_rect.height)

        x = min(0, x)
        x = max(-(self.rect.width - screen_width), x)
        y = screen_height - self.rect.height

        return pygame.Rect(x, y, width, height)

    def apply(self, window):
        return window.rect.x + self.rect.x, window.rect.y

    def update(self, window):
        self.rect = self.camera(window)

    def reset(self):
        self.rect = pygame.Rect(0, 0, self.rect.w, self.rect.height)

#import pygame as pg
#from .Vector2 import Vector2
import random
from ... import dtools


class Explosion(object):
    def __init__(self, coords):
        self.x = coords.x
        self.y = coords.y
        self.r = 20
        self.done = False

    def update(self):
        if random.random() < 0.05:
            self.done = True

    def draw(self, screen):
        if self.done: return
        dtools.circle(screen, (self.x, self.y), self.r)

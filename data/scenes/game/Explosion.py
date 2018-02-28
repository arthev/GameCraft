from .Vector2 import Vector2
from ... import dtools

MAX_SIZE = 32
FLICKER_INIT = 3

class Explosion(object):
    def __init__(self, coords):
        self.x = int(coords.x)
        self.y = int(coords.y)
        self.r = 2
        self.dr = 1
        self.flicker = FLICKER_INIT
        self.done = False

    def update(self):
        if self.r < 1: self.done = True
        self.r += self.dr
        if self.r > MAX_SIZE:
            self.r = MAX_SIZE
            self.dr *= -1

    def get_coords(self):
        return Vector2(self.x, self.y)

    def draw(self, screen):
        if self.done: return
        if self.flicker > 0: 
            self.flicker -= 1
            dtools.black_circle(screen, (self.x, self.y), self.r)
            return
        else:
            dtools.colour_circle(screen, (self.x, self.y), self.r)
            self.flicker = FLICKER_INIT

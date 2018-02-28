import math
from .Missile import Missile
from .Vector2 import Vector2
from ... import dtools

RESET_MISSILES = 10

class Base(object):
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.missiles = RESET_MISSILES

    def draw(self, screen):
#        dtools.dtext(screen, self.missiles, (self.x, self.y))
        dtools.draw_base(screen, (self.x, self.y))
    def get_distance(self, pos):
        return math.sqrt( (pos[0] - self.x)**2 +
                          (pos[1] - self.y)**2 )

    def get_coords(self):
        return Vector2(self.x, self.y)

    def shoot_missile(self, target):
        self.missiles -= 1
        return Missile(target=target, start=Vector2(self.x, self.y))

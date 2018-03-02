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
        self.done = False
        self.speed = 5

    def draw(self, screen):
        if self.done: return
        dtools.draw_base(screen, (self.x, self.y))
        dtools.draw_missile_num(screen, (self.x, self.y), self.missiles)

    def get_distance(self, pos):
        return math.sqrt( (pos[0] - self.x)**2 +
                          (pos[1] - self.y)**2 )*self.speed

    def get_coords(self):
        return Vector2(self.x, self.y)

    def shoot_missile(self, target):
        if self.missiles < 1: return
        self.missiles -= 1
        return Missile(target=target, start=Vector2(self.x, self.y), magnitude=self.speed)

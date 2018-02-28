import random
import math
from .Vector2 import Vector2
from ... import constants
from ... import dtools


class Bomb(object):
    def __init__(self, potential_targets, magnitude=1):
        self.target = random.choice(potential_targets)
        self.target_pos = self.target.get_coords()
        self.start = Vector2(random.randint(0, constants.SCREEN_SIZE[0]), constants.VOFFSET)
        self.pos = Vector2(self.start.x, self.start.y)
        self.magnitude = magnitude
        self.angle = self.target_pos - self.start
        self.angle.normalize()
        self.done = False
        self.destroyer = False

    def update(self, explosions):
        if self.done: return
        self.pos += self.angle * self.magnitude
        if self.pos.y >= self.target_pos.y:
            self.done = True
            self.destroyer = True
        for explosion in explosions:
            distance = math.sqrt( (self.pos.x - explosion.x)**2 + (self.pos.y - explosion.y)**2 )
            if distance <= explosion.r:
                self.done = True

    def get_target(self):
        return self.target

    def get_coords(self):
        return self.pos

    def draw(self, screen):
        if self.done: return
        dtools.line2(screen, self.start, self.pos)

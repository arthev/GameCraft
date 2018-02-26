from .Vector2 import Vector2
from ... import dtools

CROSS_H = 5
CROSS_W = 5

class Missile(object):
    def __init__(self, target, start=Vector2(320, 400), magnitude=5):
        self.start = start
        self.pos = Vector2(self.start.x, self.start.y)
        self.target = Vector2(target[0], target[1])
        self.magnitude = magnitude
        self.angle = self.start - self.target
        self.angle.normalize()
        self.done = False

    def update(self):
        self.pos -= self.angle * self.magnitude
        if self.pos.y <= self.target.y:
            self.done = True

    def get_coords(self):
        return self.target

    def draw(self, screen):
        if self.done: return
        dtools.line2(screen, self.start, self.pos)

        start = Vector2(self.target.x - CROSS_W, self.target.y - CROSS_H)
        end = Vector2(self.target.x + CROSS_W, self.target.y + CROSS_H)
        dtools.line2(screen, start, end)

        start.y += 2*CROSS_H
        end.y -= 2*CROSS_H
        dtools.line2(screen, start, end)

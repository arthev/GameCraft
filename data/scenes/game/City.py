from .Vector2 import Vector2
from ... import dtools

class City(object):
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def get_coords(self):
        return Vector2(self.x, self.y)


    def draw(self, screen):
        dtools.draw_city(screen, (self.x, self.y))

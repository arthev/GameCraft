import pygame as pg
import math
from .Vector2 import Vector2
from ... import constants
from ... import dtools

SZ = constants.SCREEN_SIZE

MAGNITUDE = 15

DRAW_SIZE = SZ[0]//40

TOP = constants.VOFFSET * 1.5//1
BOTTOM = 400


#Let's abuse @classmethods since only one Aim :)
class Aim(object):

    pos = Vector2(SZ[0]//2, SZ[1]//2)
    
    @classmethod
    def update(cls):
        mx, my = pg.mouse.get_pos()
        cls.target = Vector2(mx, my)
        rel = cls.target - cls.pos
        try:
            rel.normalize()
        except ZeroDivisionError:
            pass
        cls.pos += rel * MAGNITUDE

        if math.sqrt( (cls.pos.x - cls.target.x)**2 + (cls.pos.y - cls.target.y)**2 ) < MAGNITUDE:
            cls.pos.x = cls.target.x
            cls.pos.y = cls.target.y

        if cls.pos.x < 0: cls.pos.x = 0
        elif cls.pos.x > SZ[0]: cls.pos.x = SZ[0] - DRAW_SIZE
        if cls.pos.y < TOP: cls.pos.y = TOP
        elif cls.pos.y > BOTTOM: cls.pos.y = BOTTOM
        

    @classmethod
    def get_pos(cls):
        return (cls.pos.x, cls.pos.y)
        

    @classmethod
    def draw(cls, screen):
        dtools.crosshairs(screen, (cls.pos.x, cls.pos.y))
        x, y = cls.pos.x, cls.pos.y
        mx, my = cls.target.x, cls.target.y
        if x != mx or y != my:
            dtools.mouse(screen, (mx, my))


        






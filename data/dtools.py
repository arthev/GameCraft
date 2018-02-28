import pygame as pg
from . import constants
from . import settings
from .scenes.game.Vector2 import Vector2

SZ = constants.SCREEN_SIZE
BLACK = constants.BLACK

standard_font = pg.font.SysFont("Mono", constants.SCREEN_SIZE[0]//20, bold=True)

def text(msg):
    """Returns a surface of a simple text msg"""
    return standard_font.render(str(msg), False, settings.COLOUR).convert_alpha()


def arrow_surface(self, msg):
    """Returns a surface of a text msg with <> to the left"""
    t_sur = text(msg)

    h = t_sur.get_height()*0.75//1

    arrows = pg.Surface( (h, h) )
    arrows.fill(BLACK)

    pg.draw.polygon(arrows, COLOUR,
            ( (0, h//2), (h//2 - h//8, h//4), (h//2 - h//8, 3*h//4) ) )
    pg.draw.polygon(arrows, COLOUR,
            ( (h, h//2), (h//2 + h//8, h//4), (h//2 + h//8, 3*h//4) ) )

    c_sur = pg.Surface((t_sur.get_width() + arrows.get_width() + h//4,
        t_sur.get_height()))
    c_sur.fill(BLACK)
    c_sur.blit(arrows, (0, h//8))
    c_sur.blit(t_sur, (arrows.get_width() + h//4, 0))
    c_sur.convert_alpha()
    return c_sur

def line2(surface, start, end):
    def extract(pair):
        if isinstance(pair, Vector2): 
            return pair.x, pair.y
        elif isinstance(pair, tuple):
            return tuple
        elif isinstance(pair, list):
            return list[0], list[1]
    start = extract(start)
    end = extract(end)

    pg.draw.line(surface, settings.COLOUR,
            start, end, 2)

def colour_circle(surface, pos, radius):
    pg.draw.circle(surface, settings.COLOUR,
            pos, radius)
def black_circle(surface, pos, radius):
    pg.draw.circle(surface, BLACK,
            pos, radius)

def dtext(surface, msg, pos):
    t_sur = text(str(msg))
    pos = pos[0] - t_sur.get_width()//2, pos[1] - t_sur.get_height()//2
    surface.blit(t_sur, pos)

def draw_base(surface, pos):
    BW = 5*SZ[0]//80
    BH = 5*SZ[0]//160
    pg.draw.polygon(surface, settings.COLOUR,
            [(pos[0]-BW//2, pos[1]),
             (pos[0]-BW//4, pos[1]-BH),
             (pos[0]+BW//4, pos[1]-BH),
             (pos[0]+BW//2, pos[1])])

def draw_missile_num(surface, pos, num):
    t_sur = standard_font.render(str(num), False, BLACK).convert_alpha()
    surface.blit(t_sur, (pos[0] - t_sur.get_width()//2,
        SZ[1] - t_sur.get_height()*0.8//1))





def create_city_surface():
    W = SZ[0]//20
    H = SZ[1]//20
    cs = pg.Surface( (W, H) )
    def draw_block(coords):
        pg.draw.rect(cs, BLACK, coords)
        pg.draw.rect(cs, settings.COLOUR, coords, 1)
    cs.fill(constants.PUREBLACK)
    cs.set_colorkey(constants.PUREBLACK)
    draw_block((0, H//10, W//6, H))
    draw_block((W//6, H//3, W//6+W//4, H))
    draw_block((W//6+W//4, H//5, W//6+W//4+W//5, H))




    return cs.convert()
city_surface = create_city_surface()
def draw_city(surface, pos):
    x = pos[0] - city_surface.get_width()//2
    y = int(pos[1] - city_surface.get_height()*0.9)
    surface.blit(city_surface, (x, y))
def reset_city():
    global city_surface
    city_surface = create_city_surface()


CROSSHAIR_SIZE = SZ[0]//40 #Warning: Also declared in Aim.py
def crosshairs(screen, pos):
    cs = pg.Surface( (CROSSHAIR_SIZE, CROSSHAIR_SIZE) )
    cs.fill(constants.PUREBLACK)
    cs.set_colorkey(constants.PUREBLACK)
    pg.draw.line(cs, settings.COLOUR,
            (0, cs.get_height()//2), (cs.get_width(), cs.get_height()//2), 2)
    pg.draw.line(cs, settings.COLOUR,
            (cs.get_width()//2 - 1, 0), (cs.get_width()//2 - 1, cs.get_height()), 2)
    cs = cs.convert()
    screen.blit(cs, (pos[0] - cs.get_width()//2,
                     pos[1] - cs.get_height()//2))

def mouse(screen, pos):
    ms = pg.Surface( (1.25*CROSSHAIR_SIZE//1, 1.25*CROSSHAIR_SIZE//1) )
    ms.fill(constants.PUREBLACK)
    ms.set_colorkey(constants.PUREBLACK)
    mh = ms.get_height()
    mw = ms.get_width()

    pg.draw.rect(ms, settings.COLOUR,
            (0, 0, mw - 1, mh - 1), 2)
    pg.draw.line(ms, constants.PUREBLACK,
            (0, mh//4), (0, 3*mh//4), 2)
    pg.draw.line(ms, constants.PUREBLACK,
            (mw//4, 0), (3*mw//4, 0), 2)
    pg.draw.line(ms, constants.PUREBLACK,
            (mw-2, mh//4), (mw-2, 3*mh//4), 2)
    pg.draw.line(ms, constants.PUREBLACK,
            (mw//4, mh - 2), (3*mw//4, mh - 2), 2)



    ms = ms.convert()
    screen.blit(ms, (pos[0] - ms.get_width()//2, 
                     pos[1] - ms.get_height()//2))














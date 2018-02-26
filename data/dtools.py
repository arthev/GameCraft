import pygame
from . import constants
from . import settings
from .scenes.game.Vector2 import Vector2

standard_font = pygame.font.SysFont("Mono", constants.SCREEN_SIZE[0]//20, bold=True)

def text(msg):
    """Returns a surface of a simple text msg"""
    return standard_font.render(msg, False, settings.COLOUR).convert_alpha()


def arrow_surface(self, msg):
    """Returns a surface of a text msg with <> to the left"""
    t_sur = text(msg)

    h = t_sur.get_height()*0.75//1

    arrows = pygame.Surface( (h, h) )
    arrows.fill(BLACK)

    pygame.draw.polygon(arrows, COLOUR,
            ( (0, h//2), (h//2 - h//8, h//4), (h//2 - h//8, 3*h//4) ) )
    pygame.draw.polygon(arrows, COLOUR,
            ( (h, h//2), (h//2 + h//8, h//4), (h//2 + h//8, 3*h//4) ) )

    c_sur = pygame.Surface((t_sur.get_width() + arrows.get_width() + h//4,
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

    pygame.draw.line(surface, settings.COLOUR,
            start, end, 2)

def circle(surface, pos, radius):
    pygame.draw.circle(surface, settings.COLOUR,
            pos, radius)

def dtext(surface, msg, pos):
    t_sur = text(str(msg))
    pos = pos[0] - t_sur.get_width()//2, pos[1] - t_sur.get_height()//2
    surface.blit(t_sur, pos)








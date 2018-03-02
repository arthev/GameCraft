import pygame as pg
import random
from ._Overlay_Scene import _Overlay_Scene
from .. import constants
from .. import settings

BLACK = constants.BLACK
COLOUR = settings.COLOUR
SCREEN_SIZE = constants.SCREEN_SIZE
HW = constants.HW
HH = constants.HH

class Splash_Screen(_Overlay_Scene):
    def __init__(self):
        display_font = pg.font.SysFont("Mono", SCREEN_SIZE[0]//14, bold=True)
        self.display_text = display_font.render("MissilyMissileCommand", False, COLOUR, BLACK).convert()
        display_font2 = pg.font.SysFont("Mono", SCREEN_SIZE[0]//18, bold=True)
        self.display_text2 = display_font2.render("by: Arthur", False, COLOUR, BLACK).convert()
        self.lines = [i for i in range(SCREEN_SIZE[0])]
        random.shuffle(self.lines)

    def update(self):
        try:
            self.lines.pop()
            while random.random() < 0.25:
                self.lines.pop()
            pg.time.wait(8)
        except IndexError:
            pg.time.wait(1200)
            self.cont()

    def draw(self, screen):
        screen.fill(BLACK)
        screen.blit(self.display_text, 
                (HW - self.display_text.get_width()//2,
                 HH - self.display_text.get_height()))
        screen.blit(self.display_text2,
                (HW, HH))
        for line in self.lines:
            pg.draw.line(screen, BLACK, (line, 0), (line, SCREEN_SIZE[1]))

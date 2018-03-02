import pygame as pg
from .._Scene import _Scene
from ..Scene_Stack import Scene_Stack
from .. import settings
from .. import constants

SCREEN_SIZE = constants.SCREEN_SIZE

class _Overlay_Scene(_Scene):
    def cont(self): 
        Scene_Stack.pop_scene()

    def __init__(self):
        self.background = pg.display.get_surface().copy()
        self.overlay = pg.Surface(SCREEN_SIZE, pg.SRCALPHA)
        pg.draw.rect(self.overlay, (0, 0, 0, 205), (0, 0, SCREEN_SIZE[0], SCREEN_SIZE[1]))

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.overlay, (0, 0))

    def handle_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == settings.pause_button or event.key == pg.K_RETURN:
                self.cont()
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.cont()

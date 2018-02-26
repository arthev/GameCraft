import pygame as pg
from .Missile import Missile
from .Explosion import Explosion
from .Base import Base
from ..._Scene import _Scene
from ...Scene_Stack import Scene_Stack
from ... import settings
from ... import constants

COLOUR = settings.COLOUR
BLACK = constants.BLACK
SZ = constants.SCREEN_SIZE
MISSILE_REACH = 400
BASE_COORDS = [(SZ[0]//10,   19*SZ[1]//20),
               (SZ[0]//2,    19*SZ[1]//20),
               (9*SZ[0]//10, 19*SZ[1]//20)]

def ef(): pass

class Game_Scene(_Scene):
    def __init__(self):
        self.missiles = []
        self.explosions = []
        self.bases = [Base(pos) for pos in BASE_COORDS]
    
    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.pos[1] < MISSILE_REACH:
                bases = {base: base.get_distance(event.pos) for base in self.bases}
                missile = min(bases, key=bases.get).shoot_missile(event.pos)
                self.missiles.append(missile)

    def update(self):
        for missile in self.missiles: missile.update()
        for i in range(len(self.missiles) - 1, -1, -1):
            if self.missiles[i].done:
                missile = self.missiles.pop(i)
                self.explosions.append(Explosion(missile.get_coords()))
        for explosion in self.explosions: explosion.update()
        for i in range(len(self.explosions) -1, -1, -1):
            if self.explosions[i].done:
                self.explosions.pop(i)


    def draw(self, screen):
        screen.fill(BLACK)
        for missile in self.missiles: missile.draw(screen)
        for explosion in self.explosions: explosion.draw(screen)
        for base in self.bases: base.draw(screen)

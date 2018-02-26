import pygame as pg
from .Missile import Missile
from .Explosion import Explosion
from ..._Scene import _Scene
from ...Scene_Stack import Scene_Stack
from ... import settings
from ... import constants

COLOUR = settings.COLOUR
BLACK = constants.BLACK
MISSILE_REACH = 400

def ef(): pass

class Game_Scene(_Scene):
    def __init__(self):
        self.missiles = []
        self.explosions = []
    
    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.pos[1] < MISSILE_REACH:
                self.missiles.append(Missile(event.pos))

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

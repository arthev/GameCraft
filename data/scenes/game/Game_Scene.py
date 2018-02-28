import pygame as pg
import random
from .Missile import Missile
from .Explosion import Explosion
from .Base import Base
from .City import City
from .Bomb import Bomb
from .Aim import Aim
from .Game_Over import Game_Over
from ..Pause import Pause
from ..._Scene import _Scene
from ...Scene_Stack import Scene_Stack
from ... import settings
from ... import constants
from ... import dtools

COLOUR = settings.COLOUR
BLACK = constants.BLACK
SZ = constants.SCREEN_SIZE
HW = SZ[0]//2

MISSILE_REACH = 400

MAX_DELAY = 2500
MIN_DELAY = 200


BOMB_POINTS = 25

PH = 39*SZ[1]//40
BASE_COORDS = [(SZ[0]//20,   PH),
               (SZ[0]//2,    PH),
               (19*SZ[0]//20,PH)]

CITY_COORDS = [(3*SZ[0]//20, PH),
               (7*SZ[0]//20, PH),
               (8*SZ[0]//20, PH),
               (13*SZ[0]//20,PH),
               (15*SZ[0]//20,PH),
               (17*SZ[0]//20,PH)]

game_background = dtools.create_game_background()

def ef(): pass

class Game_Scene(_Scene):
    def get_multiplier(self):
        return min(6, (self.wave+1)//2)

    def get_bomb_num(self):
        return min(30, max(4, self.wave*2))

    def __init__(self, score=0, wave=1):
        self.missiles = []
        self.explosions = []
        self.bases = [Base(pos) for pos in BASE_COORDS]
        self.cities = [City(pos) for pos in CITY_COORDS]
        self.bombs = []
        self.score = score
        self.wave = wave
        self.to_bomb = [Bomb(self.bases + self.cities, self.wave) for i in range(self.get_bomb_num())]
        self.delay = random.randint(500, 2000)/1000
        self.bombs_clear = False


    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            active_bases = [base for base in self.bases if base.missiles > 0]
            bases = {base: base.get_distance(Aim.get_pos()) for base in active_bases}
            try:
                missile = min(bases, key=bases.get).shoot_missile(Aim.get_pos())
                self.missiles.append(missile)
            except ValueError:
                pass
        elif event.type == pg.KEYDOWN and event.key == settings.pause_button:
            Scene_Stack.add_scene(Pause())

    def update(self, time_passed):
        self.delay -= time_passed
        if self.delay < 0 and not self.bombs_clear:
            self.delay = random.randint(MIN_DELAY, MAX_DELAY)
            try:
                self.bombs.append(self.to_bomb.pop())
            except IndexError:
                self.bombs_clear = True
                print("Okay, bombs clear.")

        Aim.update()
        for missile in self.missiles: missile.update()
        for i in range(len(self.missiles) - 1, -1, -1):
            if self.missiles[i].done:
                missile = self.missiles.pop(i)
                self.explosions.append(Explosion(missile.get_coords()))
        for explosion in self.explosions: explosion.update()
        for i in range(len(self.explosions) -1, -1, -1):
            if self.explosions[i].done:
                self.explosions.pop(i)
        for bomb in self.bombs: bomb.update(self.explosions)
        for i in range(len(self.bombs) -1, -1, -1):
            if self.bombs[i].done:
                bomb = self.bombs.pop(i)
                self.explosions.append(Explosion(bomb.get_coords()))
                if bomb.destroyer:
                    try: self.bases.remove(bomb.get_target())
                    except ValueError: pass
                    try: self.cities.remove(bomb.get_target())
                    except ValueError: pass
                else:
                    self.score += BOMB_POINTS * self.get_multiplier()

        #Let's check for game state changes, heh.
        active_bases = [base for base in self.bases if base.missiles > 0]
        if not active_bases:
            #game over
            #TODO: The check here is actually harder: Must be impossible to remove all the bombs with the missiles already in flight, so the check needs a redo.
            Scene_Stack.change_scene(Game_Over(self.bases + self.cities, self.bombs, self.score))



    def draw(self, screen):
        screen.blit(game_background, (0, 0))
        dtools.dtext(screen, self.score, (HW, constants.VOFFSET//2))
        for missile in self.missiles: missile.draw(screen)
        for explosion in self.explosions: explosion.draw(screen)
        for base in self.bases: base.draw(screen)
        for city in self.cities: city.draw(screen)
        for bomb in self.bombs: bomb.draw(screen)
        Aim.draw(screen)

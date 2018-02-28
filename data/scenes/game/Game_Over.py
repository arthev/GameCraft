import pygame as pg
import random
from .Bomb import Bomb
from .Vector2 import Vector2
from ..._Scene import _Scene
from ...Scene_Stack import Scene_Stack
from ... import dtools
from ... import constants
from ... import settings

class Mock(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def get_coords(self):
        return Vector2(self.x, self.y)
    def draw(self, screen):
        pass


game_background = dtools.create_game_background()
class Game_Over(_Scene):
    def create_overlay(self):
        r, g, b = settings.COLOUR
        ol = pg.Surface(constants.SCREEN_SIZE, pg.SRCALPHA)
        pg.draw.rect(ol, (r, g, b, 0), (0, 0, constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1]))
        ol = ol.convert()
        ol.set_alpha(0)
        return ol

    def __init__(self, hubs, bombs, score):
        self.score = score
        self.hubs = hubs + [Mock(random.randint(-200, constants.SCREEN_SIZE[0] + 200), constants.SCREEN_SIZE[1]) for i in range(100)]
        self.bombs = bombs
        self.i = 0
        self.overlay = self.create_overlay()
        self.delay = 15000

    def update(self, time_passed):
        self.delay -= time_passed
        if self.delay < 13000 and random.random() < 0.2:
            self.bombs.append(Bomb(self.hubs, 100))
        if self.delay < 1100 and random.random() < 0.4:
            self.bombs.append(Bomb(self.hubs, 100))

        if self.delay < 8000 and random.random() < 0.6:
            self.bombs.append(Bomb(self.hubs, 100))
        if self.delay < 5000 and random.random() < 0.8:
            self.bombs.append(Bomb(self.hubs, 100))
        if self.delay < 3000:
            self.bombs.append(Bomb(self.hubs, 100))




        if self.delay < 0:
            self.i += 3
            if self.i > 255: self.i = 255
            self.overlay.set_alpha(self.i)
        if self.i == 255:
            pg.time.wait(2000)
            #TODO: Send to high score, hehe.
            Scene_Stack.change_scene(Fade_Out(self.score))
        for bomb in self.bombs: bomb.update([])


    def draw(self, screen):
        screen.blit(game_background, (0, 0))
        dtools.dtext(screen, self.score, (constants.HW, constants.VOFFSET//2))
        for hub in self.hubs: hub.draw(screen)
        for bomb in self.bombs:
            bomb.done = False
            bomb.draw(screen)
        
        screen.blit(self.overlay, (0, 0))


class Fade_Out(_Scene):
    def __init__(self, score):
        self.score = score
        self.overlay = self.create_overlay()
        self.i = 0


    def create_overlay(self):
        ol = pg.Surface(constants.SCREEN_SIZE, pg.SRCALPHA)
        pg.draw.rect(ol, (0, 0, 0, 0), (0, 0, constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1]))
        ol = ol.convert()
        ol.set_alpha(0)
        return ol

    def update(self):
        self.i += 1
        self.overlay.set_alpha(self.i)
        pg.time.wait(10)
        if self.i > 255:
            pg.time.wait(1000)
            Scene_Stack.pop_scene()

    def draw(self, screen):
        screen.fill(settings.COLOUR)
        screen.blit(self.overlay, (0, 0))



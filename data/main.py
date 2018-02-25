import pygame as pg
from . import setup
from . import constants
from .Scene_Stack import Scene_Stack
from .scenes.Main_Menu import Main_Menu

TIME_PER_UPDATE = 1000.0/constants.FPS

def main(): 
    Scene_Stack.add_scene(Main_Menu())
    driver = Driver()
    driver.main()


class Driver(object):
    def __init__(self):
        self.finished = False
        self.clock = pg.time.Clock()
        self.fps = constants.FPS
        self.screen = pg.display.get_surface()

    def main(self):
        """This is the main loop of the entire program."""
        delay = 0.0
        while not self.finished:
            delay += self.clock.tick(self.fps)
            self.current_scene = Scene_Stack.get_current()
            if self.current_scene == None:
                self.finished = True
            elif delay >= TIME_PER_UPDATE:
                self.event_loop()
                self.update(delay)
                self.draw()
                delay = 0.0

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.constants.QUIT:
                self.finished = True
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.finished = True
            else:
                self.current_scene.handle_event(event)

    def update(self, delay):
        pass

    def draw(self):
        self.current_scene.draw(self.screen)
        pg.display.update()

















import pygame as pg
import json
from .Highscore_View import Highscore_View
from .. import constants
from .. import dtools
from .. import settings
from .._Scene import _Scene
from ..Scene_Stack import Scene_Stack

import pprint
pp = pprint.PrettyPrinter()

class Highscore_Entry(_Scene):
    def save_scores(self):
        with open(str(constants.HIGHSCORE_PATH), 'w') as score_file:
            json.dump(settings.high_scores, score_file)

    def no_score(self):
        #Remove self;implicitly return to main menu
        Scene_Stack.pop_scene()

    def yes_score(self):
        settings.high_scores[self.hit] = {"name":self.name, "score":self.score}
        self.save_scores()
        Scene_Stack.change_scene(Highscore_View())

    def __init__(self, score):
        print("Here...")
        pp.pprint(settings.high_scores)
        if score <= settings.high_scores["5"]["score"]:
            self.done = True
            return
        else:
            self.done = False
            self.score = score
            self.hit = "5"
            for i in range(5, 0, -1):
                if score > settings.high_scores[str(i)]["score"]:
                    self.hit = str(i)
            for i in range(5, int(self.hit), -1):
                settings.high_scores[str(i)] = settings.high_scores[str(i-1)]
            self.name = ""

    def handle_event(self, event):
        if self.done: self.no_score(); return
        else:
            if event.type == pg.KEYDOWN:
                if event.unicode.isalpha():
                    self.name += event.unicode
                elif event.key == pg.K_BACKSPACE:
                    if self.name == "": pass
                    else: self.name = self.name[:-1]
                elif event.key == pg.K_RETURN:
                    self.yes_score()

    def draw(self, screen):
        if self.done: return
        screen.fill(constants.BLACK)
        dtools.dtext(screen, "New score! Enter name:", (constants.HW, constants.HH))
        dtools.dtext(screen, self.name, (constants.HW, constants.HH*6//5))

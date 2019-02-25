import json
#import os
import pygame as pg
from . import constants
from . import settings

CAPTION = "MissilyMissileCommand"

pg.init()

pg.display.set_caption(CAPTION)
pg.display.set_mode(constants.SCREEN_SIZE)

pg.mouse.set_visible(False)

def load_highscores():
    try:
        with open(str(constants.HIGHSCORE_PATH), 'r') as score_file:
            settings.high_scores = json.load(score_file)
    except FileNotFoundError:
        with open(str(constants.HIGHSCORE_PATH), 'w') as score_file:
            json.dump(settings.high_scores, score_file)
        load_highscores()
load_highscores()

def load_settings():
    try:
        with open(str(constants.SETTINGS_PATH), 'r') as settings_file:
            the_settings = json.load(settings_file)
            for k, v in the_settings.items():
                exec("settings.{var} = {val}".format(var=k, val=v))
    except FileNotFoundError:
        pass #Use sane defaults
load_settings()


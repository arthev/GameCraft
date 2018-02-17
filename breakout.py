import pygame
import random
import os
import sys
import json
from constants import *

SETTINGS_PATH = os.path.join("data", "config_breakout.cfg")
HIGHSCORE_PATH = os.path.join("data", "scores.txt")
MAP_DIR = "naps"

PADDLE_VEL = 500
PADDLE_FRICTION = 3
COLOUR = AMBER
up_button = pygame.K_UP
left_button = pygame.K_LEFT
down_button = pygame.K_DOWN
right_button = pygame.K_RIGHT
pause_button = pygame.K_p
fps = 60
lives_setting = 3


high_scores = {1:{"name":None, "score":0},
               2:{"name":None, "score":0},
               3:{"name":None, "score":0},
               4:{"name":None, "score":0},
               5:{"name":None, "score":0}}

def include(filename):
    if os.path.exists(filename):
        exec(open(filename).read(), globals())
def load_settings():
    if os.path.isfile(SETTINGS_PATH):
        with open(SETTINGS_PATH, 'r') as settings_file:
            settings = json.load(settings_file)
            for item in settings:
                globals()[item] = settings[item]
    else:
        with open(SETTINGS_PATH, 'w') as settings_file:
            json.dump({}, settings_file) #Game has sane defaults.
def load_highscore():
    if os.path.isfile(HIGHSCORE_PATH):
        with open(HIGHSCORE_PATH, 'r') as score_file:
            global high_scores
            high_scores = json.load(score_file)
    else:
        with open(HIGHSCORE_PATH, 'w') as score_file:
            json.dump(high_scores, score_file)
        load_highscore()

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
load_settings()
include("block_surfaces.py")
from Scene import *
include("menu_scenes.py")
include("overlay_scenes.py")
include("logical_scenes.py")
gfont = pygame.font.SysFont("Mono", SCREEN_SIZE[0]//20, bold=True)

VOFFSET = 3
DVOFFSET = 3 * BH

scene_stack = []

def ef(): pass
def add_scene(scene): scene_stack.append(scene)
def pop_scene(): scene_stack.pop()
def change_scene(scene): pop_scene(); add_scene(scene)

def main_loop():
    while True:
        try:
            current_scene = scene_stack[-1]
            current_scene.update()
            current_scene.draw()
            pygame.display.update()
        except IndexError:
            exit() #Scene_stack empty
if __name__ == '__main__':
    #Note: load_settings() now up with the imports and includes.
    load_highscore()
    #add_scene(Main_Menu())
    #add_scene(Splash_Screen())
    add_scene(Game_Scene())
    main_loop()

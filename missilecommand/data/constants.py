import os

#screen
SCREEN_SIZE = (640, 480)
HW = SCREEN_SIZE[0]//2
HH = SCREEN_SIZE[1]//2

VOFFSET = SCREEN_SIZE[1]//10

#colours
PUREBLACK = (0, 0, 0)
BLACK = (40, 40, 40)
AMBER = (255, 176, 0)
LTAMBER = (255, 204, 0)
GREEN1 = (51, 255, 0)
GREEN2 = (0, 255, 51)
GREEN3 = (0, 255, 102)
APPLE1 = (51, 255, 51)
APPLE2 = (102, 255, 102)
COLOURLIST = (AMBER, LTAMBER, GREEN1, GREEN2, GREEN3, APPLE1, APPLE2)

#Gamestate
FPS = 60.0

#paths
_dir_path = os.path.dirname(os.path.realpath(__file__))
HIGHSCORE_PATH = os.path.join(_dir_path, "save_data", "scores.txt")
SETTINGS_PATH = os.path.join(_dir_path, "save_data", "config.cfg")

import os
import pygame
import json
from constants import *
from tkinter import filedialog

#Checks if fn - a filename - is of type .abrm
def abrm(fn):
    fn = fn.name
    return ".abrm" == fn[fn.rfind("."):]

def open_file():
    fn = filedialog.askopenfile()
    if fn and abrm(fn):
        with open(fn.name, 'r') as f:
            global bmap
            jmap = json.load(f)
            for i in jmap:
                bmap[int(i)] = jmap[i]
    else:
        print("Couldn't open file...")

def save_file():
    fn = filedialog.asksaveasfile()
    if fn and abrm(fn):
        with open(fn.name, 'w') as f:
            json.dump(bmap, f)
    else:
        print("Couldn't save file...")


def include(filename):
    if os.path.exists(filename):
        exec(open(filename).read(),globals())

FPS = 10

COLOUR = AMBER
VOFFSET = 3

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
include('block_surfaces.py')
global_font = pygame.font.SysFont("Mono", 32, bold=True)

bmap = {i:[0 for j in range(SCREEN_SIZE[1]//BH)] for i in range(SCREEN_SIZE[0]//BW)}
clock = pygame.time.Clock()

press_key = None
press_value = None

bfo_sur = pygame.Surface((BW, VOFFSET*BH))
bfo_sur.fill(BLACK)
pygame.draw.rect(bfo_sur, COLOUR, (0, 0, BW, VOFFSET*BH), 2)

s_sur = bfo_sur.copy()
f_tex = global_font.render("S", False, COLOUR)
s_sur.blit(f_tex, (BW//2 - f_tex.get_width()//2, VOFFSET*BH//2 - f_tex.get_height()//2))
s_sur = s_sur.convert()

f_tex = global_font.render("L", False, COLOUR)
l_sur = bfo_sur.copy()
l_sur.blit(f_tex, (BW//2 - f_tex.get_width()//2, VOFFSET*BH//2 - f_tex.get_height()//2))
l_sur = l_sur.convert()

f_tex = global_font.render("N", False, COLOUR)
n_sur = bfo_sur.copy()
n_sur.blit(f_tex, (BW//2 - f_tex.get_width()//2, VOFFSET*BH//2 - f_tex.get_height()//2))
n_sur = n_sur.convert()


while True:
    clock.tick(FPS)

    x, y = pygame.mouse.get_pos()
    x //= BW
    y//= BH
    y -= 3
    pos = x, y

    for event in pygame.event.get():
        if event.type == pygame.constants.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()
            elif event.unicode.isdigit():
                v = int(event.unicode)
                if v <= max(block_surfaces):
                    press_key = True
                    press_value = v
        elif event.type == pygame.KEYUP:
            v = pygame.key.name(event.key)
            if v.isdigit() and int(v) == press_value:
                press_key = False
    if pygame.mouse.get_pressed()[0]:
        if y >= 0:
            #Time to 'draw' on the map!
            a=bmap[x][y]
            if a == max(block_surfaces):
                bmap[x][y]=0
            else: 
                bmap[x][y] += 1
        else:
            if x == 0: save_file()
            elif x==1: open_file()
            elif x==2:
                bmap = {i:[0 for j in range(SCREEN_SIZE[1]//BH)] for i in range(SCREEN_SIZE[0]//BW)}


    if press_key:
        bmap[x][y] = press_value

    #Draw
#    text = global_font.render("Pos:" + str(pos), False, COLOUR)
    screen.fill(BLACK)
#    screen.blit(text, (HW, HH))
    pygame.draw.line(screen, COLOUR, (0, VOFFSET * BH - 2), (SCREEN_SIZE[0], VOFFSET * BH - 2))
    for i in bmap:
        for j, e in enumerate(bmap[i]):
            if e == 0: continue
            screen.blit(block_surfaces[e], 
                    (i*BW, (j+VOFFSET)*BH))
    screen.blit(s_sur, (0, 0))
    screen.blit(l_sur, (BW,0))
    screen.blit(n_sur, (2*BW, 0))

    pygame.display.update()

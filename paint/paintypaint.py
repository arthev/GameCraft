#import os
import sys
import pygame as pg
import json
from tkinter import Tk, filedialog, simpledialog

def quit(): pg.quit(); sys.exit()

SCREEN_SIZE = (800, 800)
FPS = 60
VOFFSET = 64 #This is in pixels directly
HOFFSET = 64 #Same
BLACK = (0, 0, 0)
COLOUR = AMBER = (255, 176, 0)
LGRAY = (180, 180, 180) #For use as transparent
DGRAY = (120, 120, 120) #Same

#Here comes the file handlers
def pmp(fn) -> bool: #fn -> filename
    fn = fn.name
    return ".pmp" == fn[fn.rfind("."):]

def open_file():
    root = Tk()
    root.withdraw()
    root.update()
    fn = filedialog.askopenfile()
    if fn and pmp(fn):
        with open(fn.name, 'r') as f:
            global pmap
            pmap = {} #Reset to avoid mismatch on sizes
            jmap = json.load(f)
            for i in jmap:
                pmap[int(i)] = jmap[i]
    else:
        print("Couldn't open file...")
    root.update()
    root.destroy()

def save_file():
    root = Tk()
    root.withdraw()
    root.update()
    fn = filedialog.asksaveasfile()
    if fn and pmp(fn):
        with open(fn.name, 'w') as f:
            json.dump(pmap, f)
    else:
        print("Couldn't save file...")
    root.update()
    root.destroy()

def new_pmap():
    global pmap
    root = Tk()
    root.withdraw()
    root.update()
    size = simpledialog.askinteger("Pmap size", "n*n pixels -> input n", initialvalue=16)
    pmap = {i:["t" for i in range(size)] for i in range(size)}
    root.update()
    root.destroy()

def set_pixel(x, y):
    try:
        pmap[x][y] = current_substance
    except IndexError:
        pass
    except KeyError:
        pass

class Button(object):
    def create_buttony_surface(self, msg):
        f_tex = gfont.render(msg, False, COLOUR)
        bg_sur = pg.Surface( (HOFFSET, VOFFSET) )
        bg_sur.fill(BLACK)
        pg.draw.rect(bg_sur, COLOUR, (0, 0, bg_sur.get_width(), VOFFSET), 2)
        bg_sur.blit(f_tex, (bg_sur.get_width()//2 - f_tex.get_width()//2, bg_sur.get_height()//2 - f_tex.get_height()//2))
        return bg_sur.convert()

    def __init__(self, msg, func, x, y):
        self.surface = self.create_buttony_surface(msg)
        self.func = func
        self.x = x
        self.y = y
        self.w = self.surface.get_width()
        self.h = self.surface.get_height()

    def draw(self, screen):
        screen.blit(self.surface, (self.x, self.y))


pg.init()
screen = pg.display.set_mode(SCREEN_SIZE)
gfont = pg.font.SysFont("Mono", 32, bold=True)
clock = pg.time.Clock()

save_button = Button("S", save_file, HOFFSET, 0)
load_button = Button("L", open_file, save_button.x + save_button.w, 0)
new_button = Button("N", new_pmap, load_button.x + load_button.w, 0)
buttons = [save_button, load_button, new_button]

pmap = None; new_pmap()
current_substance = "t"
press_key = False

while True:
    clock.tick(FPS)

    pw = (SCREEN_SIZE[0] - 2*HOFFSET)//len(pmap)
    ph = (SCREEN_SIZE[1] - 2*VOFFSET)//len(pmap[0])

    p_sur = pg.Surface( (pw, ph) )

    mx, my = pg.mouse.get_pos()
    x = int((mx-HOFFSET)//pw)
    y = int((my-VOFFSET)//ph)
   
    #Handle_Event
    for event in pg.event.get():
        if event.type == pg.constants.QUIT:
            quit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                quit()
            elif event.unicode.isdigit():
                v = int(event.unicode)
                legals = {1: "c", 2: "b", 3:"t"}
                if v in legals:
                    press_key = True
                    current_substance = legals[v]
        elif event.type == pg.KEYUP:
            press_key = False

    #Update 
    if press_key: 
        if x >= 0 and y >= 0 and x < len(pmap) and y < len(pmap[0]):
            set_pixel(x, y)
    if pg.mouse.get_pressed()[0]:
        if x >= 0 and y >= 0 and x < len(pmap) and y < len(pmap[0]):
            set_pixel(x, y)
        else:
            for button in buttons:
                if mx > button.x and mx < button.x + button.w and my > button.y and my < button.y + button.h:
                    button.func()

    #Draw
    screen.fill(BLACK)
    pg.draw.line(screen, COLOUR, (0, VOFFSET - 2), (SCREEN_SIZE[0], VOFFSET - 2), 2)
    pg.draw.line(screen, COLOUR, (0, SCREEN_SIZE[1] - VOFFSET), (SCREEN_SIZE[0], SCREEN_SIZE[1] - VOFFSET), 2)
    pg.draw.line(screen, COLOUR, (HOFFSET - 2, 0), (HOFFSET - 2, SCREEN_SIZE[1]), 2)
    pg.draw.line(screen, COLOUR, (SCREEN_SIZE[0] - HOFFSET, 0), (SCREEN_SIZE[0] - HOFFSET, SCREEN_SIZE[1]), 2)

    def draw_pixel(col):
        x = HOFFSET + i*pw
        y = VOFFSET + j*ph
        p_sur.fill(col)
        screen.blit(p_sur, (x, y))

    for i in pmap:
        for j, e in enumerate(pmap[i]):
            if e == "b":
                draw_pixel(BLACK)
            elif e == "c":
                draw_pixel(COLOUR)
            elif e == "t":
                if (i + j) % 2 == 0:
                    draw_pixel(LGRAY)
                else:
                    draw_pixel(DGRAY)

    for button in buttons: button.draw(screen)

    pg.display.update()

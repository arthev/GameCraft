import os
import pygame
from constants import *
#from block_surfaces import *

def include(filename):
    if os.path.exists(filename):
       exec(open(filename).read(),globals())
       

HW = SCREEN_SIZE[0]//2
HH = SCREEN_SIZE[1]//2

BLACK = (40, 40, 40)
COLOUR = AMBER = (255, 176, 0)

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
include('block_surfaces.py')

screen.fill(BLACK)
screen.blit(block_surfaces[1], (HW, HH))
screen.blit(block_surfaces[2], (HW, HH - BH))
screen.blit(block_surfaces[3], (HW, HH - 2*BH))
screen.blit(block_surfaces[4], (HW, HH + BH))
screen.blit(block_surfaces[5], (HW, HH + 2*BH))
screen.blit(block_surfaces[6], (HW, HH + 3*BH))

pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()


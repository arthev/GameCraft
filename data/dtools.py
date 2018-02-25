import pygame
from . import constants
from . import settings

standard_font = pygame.font.SysFont("Mono", constants.SCREEN_SIZE[0]//20, bold=True)

def text(msg):
    return standard_font.render(msg, False, settings.COLOUR).convert_alpha()



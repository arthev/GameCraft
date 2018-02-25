import pygame as pg
from .._Scene import _Scene
from .. import settings
from .. import dtools
from .. import constants

HH = constants.HH
HW = constants.HW
BLACK = constants.BLACK

MENU_DWINDLE = 0.6

class _Menu_Scene(_Scene):
    #set "surface":None in an option dict for standard display.
    def __init__(self, options):
        self.selection = 0
        self.options = options

    def get_select_up(self, from_i=None) -> int:
        i = self.selection if from_i == None else from_i
        return len(self.options) -  1 if i == 0 else i - 1
    def get_select_down(self, from_i=None) -> int:
        i = self.selection if from_i == None else from_i
        return 0 if i == len(self.options) - 1 else i + 1
    def select_up(self):
        self.selection = self.get_select_up()
    def select_down(self):
        self.selection = self.get_select_down()

    def select_right(self):
        cur = self.options[self.selection]
        if "right" in cur: cur["right"]()
    def select_left(self):
        cur = self.options[self.selection]
        if "left" in cur: cur["left"]()

    def call_selected(self):
        cur = self.options[self.selection]
        if "var" in cur: cur["func"](cur)
        else: cur["func"]()

    def handle_event(self, event):
        dispatch = {settings.up_button: self.select_up,
                    settings.down_button: self.select_down,
                    settings.right_button: self.select_right,
                    settings.left_button: self.select_left,
                    settings.select_button: self.call_selected}
        if event.type == pg.KEYDOWN:
            if event.key in dispatch:
                dispatch[event.key]()

    def get_option_surface(self, opt):
        if "surface" not in opt or not opt["surface"]: return dtools.text(opt["text"])
        elif "var" in opt: return opt["surface"](opt)
        else: return opt["surface"]()

    def draw(self, screen):
        screen.fill(BLACK)

        c_sur = self.get_option_surface(self.options[self.selection])
        screen.blit(c_sur, (HW - c_sur.get_width()//2, 
                            HH - c_sur.get_height()//2))
        
        a_sur = self.get_option_surface(self.options[self.get_select_up()])
        a_sur = pg.transform.smoothscale(a_sur, (round(a_sur.get_width()*MENU_DWINDLE),
                                                    (round(a_sur.get_height()*MENU_DWINDLE))))
        screen.blit(a_sur, (HW - a_sur.get_width()//2,
                            HH - a_sur.get_height() * 2))

        b_sur = self.get_option_surface(self.options[self.get_select_down()])
        b_sur = pg.transform.smoothscale(b_sur, (round(b_sur.get_width()*MENU_DWINDLE),
                                                    (round(b_sur.get_height()*MENU_DWINDLE))))
        screen.blit(b_sur, (HW - b_sur.get_width()//2,
                              HH + b_sur.get_height()))

        aa_sur = self.get_option_surface(self.options[self.get_select_up(self.get_select_up())])
        aa_sur = pg.transform.smoothscale(aa_sur, (round(aa_sur.get_width()*MENU_DWINDLE*MENU_DWINDLE),
                                                      round(aa_sur.get_height()*MENU_DWINDLE*MENU_DWINDLE)))
        screen.blit(aa_sur, (HW - aa_sur.get_width()//2,
                             HH - a_sur.get_height() * 2 - aa_sur.get_height() * 2))

        bb_sur = self.get_option_surface(self.options[self.get_select_down(self.get_select_down())])
        bb_sur = pg.transform.smoothscale(bb_sur, (round(bb_sur.get_width()*MENU_DWINDLE*MENU_DWINDLE),
                                                      round(bb_sur.get_height()*MENU_DWINDLE*MENU_DWINDLE)))
        screen.blit(aa_sur, (HW - aa_sur.get_width()//2,
                             HH + b_sur.get_height() * 2 + bb_sur.get_height()))

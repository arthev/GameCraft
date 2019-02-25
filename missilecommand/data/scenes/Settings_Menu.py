import pygame as pg
import json
from ._Menu_Scene import _Menu_Scene
from .Set_Key import Set_Key
from .game import Game_Scene
from .game import Game_Over
from .. import constants
from .. import dtools
from .. import settings
from ..Scene_Stack import Scene_Stack

def ef(): pass

class Settings_Menu(_Menu_Scene):
    def save_settings(self):
        with open(str(constants.SETTINGS_PATH), 'w') as settings_file:
            current_settings = {
                    "COLOUR": settings.COLOUR,
                    "up_button": settings.up_button,
                    "down_button": settings.down_button,
                    "left_button": settings.left_button,
                    "right_button": settings.right_button,
                    "select_button": settings.select_button,
                    "pause_button": settings.pause_button
                    }


            json.dump(current_settings, settings_file)

    def exit_settings(self):
        self.save_settings()

        #Manually update a few things
        dtools.missile_surface = dtools.create_missile_surface()
        dtools.city_surface = dtools.create_city_surface()
        Game_Scene.game_background = dtools.create_game_background()
        Game_Over.game_background = dtools.create_game_background()


        Scene_Stack.pop_scene()

    def set_key(self, specifier):
        Scene_Stack.add_scene(Set_Key(specifier))
    def key_surface(self, specifier):
        key_name = pg.key.name(eval("settings.{var}".format(var=specifier["var"])))
        return dtools.text(specifier["text"] + key_name)

    def colour_surface(self):
        return dtools.arrow_surface("Colour")
    def colour_right(self):
        if self.colour_selection == len(constants.COLOURLIST) - 1:
            self.colour_selection = 0
        else: 
            self.colour_selection += 1
        settings.COLOUR = constants.COLOURLIST[self.colour_selection]
    def colour_left(self):
        if self.colour_selection == 0:
            self.colour_selection = len(constants.COLOURLIST) - 1
        else:
            self.colour_selection -= 1
        settings.COLOUR = constants.COLOURLIST[self.colour_selection]

    def __init__(self):
        self.colour_selection = 0
        for i, colour in enumerate(constants.COLOURLIST):
            if colour == settings.COLOUR:
                self.colour_selection = i
        options = [
                {"text":"Colour", "func": ef, "surface": self.colour_surface, "right": self.colour_right, "left": self.colour_left},

                {"text":"Up: ", "func": self.set_key, "var": "up_button", "surface": self.key_surface},
                {"text":"Down: ", "func": self.set_key, "var": "down_button", "surface": self.key_surface},
                {"text":"Left: ", "func": self.set_key, "var": "left_button", "surface": self.key_surface},
                {"text":"Right: ", "func": self.set_key, "var": "right_button", "surface": self.key_surface},
                {"text":"Pause: ", "func": self.set_key, "var": "pause_button", "surface": self.key_surface},
                {"text":"Select: ", "func": self.set_key, "var": "select_button", "surface": self.key_surface},
                {"text":"Exit", "func": self.exit_settings}]
        super().__init__(options)


















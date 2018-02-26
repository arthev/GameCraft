from ._Menu_Scene import _Menu_Scene
from .Settings_Menu import Settings_Menu
from .game.Game_Scene import Game_Scene
from ..Scene_Stack import Scene_Stack

def ef(): pass

class Main_Menu(_Menu_Scene):
    def goto_settings(self): Scene_Stack.add_scene(Settings_Menu())
    def goto_game(self): Scene_Stack.add_scene(Game_Scene())
        

    def __init__(self):
        options = [{"text":"Play", "func": self.goto_game},
                   {"text":"High Score", "func": ef},
                   {"text":"Settings", "func": self.goto_settings},
                   {"text":"Exit", "func": ef}]
        super().__init__(options)

from ._Menu_Scene import _Menu_Scene
from .Highscore_View import Highscore_View
from .Settings_Menu import Settings_Menu
from .game.Game_Scene import Game_Scene
from ..Scene_Stack import Scene_Stack

from .. import dtools

def ef(): pass

class Main_Menu(_Menu_Scene):
    def goto_settings(self): Scene_Stack.add_scene(Settings_Menu())
    def goto_game(self): Scene_Stack.add_scene(Game_Scene())
    def goto_exit(self): Scene_Stack.pop_scene()
    def goto_highscore(self): Scene_Stack.add_scene(Highscore_View())
        

    def __init__(self):
        options = [{"text":"Play", "func": self.goto_game},
                   {"text":"High Score", "func": self.goto_highscore},
                   {"text":"Settings", "func": self.goto_settings},
                   {"text":"Exit", "func": self.goto_exit}]
        super().__init__(options)


    def draw(self, screen):
        super().draw(screen)

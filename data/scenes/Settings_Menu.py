from ._Menu_Scene import _Menu_Scene
from ..Scene_Stack import Scene_Stack

def ef(): pass

class Settings_Menu(_Menu_Scene):
    def exit_settings(self):
        Scene_Stack.pop_scene()

    def __init__(self):
        options = [{"text":"Dummy", "func": ef},
                   {"text":"Dummydum", "func": ef},
                   {"text":"Dummydumdum", "func": ef},
                   {"text":"Exit", "func": self.exit_settings}]
        super().__init__(options)

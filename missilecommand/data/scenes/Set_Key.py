from ._Overlay_Scene import _Overlay_Scene
from .. import constants
from .. import dtools
from .. import settings
from ..Scene_Stack import Scene_Stack

class Set_Key(_Overlay_Scene):
    def cont(self, key_val):
        exec("settings.{var} = {val}".format(var=self.specified, val=key_val))
        Scene_Stack.pop_scene()

    def __init__(self, specified):
        self.specified = specified["var"]
        super().__init__()

    def draw(self, screen):
        super().draw(screen)
        dtools.dtext(screen, "Press desired key...", (constants.HW, constants.HH))

    def handle_event(self, event):
        if event.key != settings.pause_button and event.key != settings.select_button:
            self.cont(event.key)

from ._Overlay_Scene import _Overlay_Scene
from .. import dtools
from .. import constants

class Pause(_Overlay_Scene):
    def draw(self, screen):  
        super().draw(screen)
        dtools.dtext(screen, "Paused", (constants.HW, constants.HH))

from ._Overlay_Scene import _Overlay_Scene
from .. import dtools
from ..constants import SCREEN_SIZE, BLACK
from ..settings import high_scores, COLOUR



class Highscore_View(_Overlay_Scene):
    def draw(self, screen):
        screen.fill(BLACK)
        fifth = SCREEN_SIZE[1]//5
        for i in high_scores:
            name = high_scores[i]["name"]
            if name == None: name = ""
            score = high_scores[i]["score"]
            t_sur = dtools.text("{:6} : {}".format(score, name))
            screen.blit(t_sur, (SCREEN_SIZE[0]//6, (int(i)-1)*fifth + fifth//3))
            





from .._Overlay_Scene import _Overlay_Scene

class Board_Cleared(_Overlay_Scene):
    def __init__(self, score_diff, cities, bases):
        super().__init__()




    def draw(self, screen):
        super().draw(screen)
#        text = gfont.render("Board Cleared! Well done!", False, COLOUR).convert_alpha()
#        screen.blit(text, (HW - text.get_width()//2,
#                           HH-text.get_height()//2 - gfont.get_linesize()//2))
#        infotext = gfont.render("Press Return or Pause to continue.", False, COLOUR).convert_alpha()
#        infotext = pygame.transform.scale(infotext, (round(infotext.get_width()*MENU_DWINDLE),
#                                                     round(infotext.get_height()*MENU_DWINDLE)))
#        screen.blit(infotext, (HW - infotext.get_width()//2,
#                               HH-infotext.get_height()//2 + gfont.get_linesize()//2))

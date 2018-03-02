import pygame as pg
from .._Overlay_Scene import _Overlay_Scene
from ... import dtools
from ... import constants
from ... import settings

SZ = constants.SCREEN_SIZE

class Board_Cleared(_Overlay_Scene):
    def __init__(self, score_diff, cities, bases, multiplier):
        super().__init__()
        self.score_diff = score_diff
        self.cities = len(cities)
        self.missiles = sum([base.missiles for base in bases])
        self.multiplier = multiplier

        self.c_sur = self.create_city_line()
        self.m_sur = self.create_missile_line()

    def create_city_line(self):
        c_sur = dtools.create_city_surface()
        c_sur = pg.transform.scale(c_sur, (SZ[0]//10, SZ[0]//10))
        tf = pg.font.SysFont("Mono", SZ[0]//40, bold=True)
        x_sur = tf.render(" x ", False, settings.COLOUR).convert_alpha()
        bf = pg.font.SysFont("Mono", SZ[0]//10, bold=True)
        city_score_sur = bf.render("100", False, settings.COLOUR).convert_alpha() #Magic number straight from scoring rules, hehe
        m_sur = bf.render(str(self.multiplier), False, settings.COLOUR).convert_alpha()
        n_sur = bf.render("{:>2}".format(self.cities), False, settings.COLOUR).convert_alpha()

        city_line_sur = pg.Surface( (c_sur.get_width()+3*x_sur.get_width()+n_sur.get_width() + city_score_sur.get_width() + m_sur.get_width(), bf.get_linesize()) )
        city_line_sur.fill(constants.PUREBLACK)
        city_line_sur.set_colorkey(constants.PUREBLACK)

        def gh(sur):
            return bf.get_linesize()//2 - sur.get_height()//2
        def gw(sur_list):
            return sum([sur.get_width() for sur in sur_list])
        city_line_sur.blit(c_sur, (0, gh(c_sur)))
        city_line_sur.blit(x_sur, (gw([c_sur]), gh(x_sur)))
        city_line_sur.blit(n_sur, (gw([c_sur, x_sur]), gh(n_sur)))
        city_line_sur.blit(x_sur, (gw([c_sur, x_sur, n_sur]), gh(x_sur)))
        city_line_sur.blit(city_score_sur, (gw([c_sur, x_sur, n_sur, x_sur]), gh(city_score_sur)))
        city_line_sur.blit(x_sur, (gw([c_sur, x_sur, n_sur, x_sur, city_score_sur]), gh(x_sur)))
        city_line_sur.blit(m_sur, (gw([c_sur, x_sur, n_sur, x_sur, city_score_sur, x_sur]), gh(m_sur)))

        return city_line_sur.convert_alpha()

    def create_missile_line(self):
        c_sur = dtools.create_missile_surface()
        c_sur = pg.transform.scale(c_sur, (SZ[0]//10, SZ[0]//10))
        tf = pg.font.SysFont("Mono", SZ[0]//40, bold=True)
        x_sur = tf.render(" x ", False, settings.COLOUR).convert_alpha()
        bf = pg.font.SysFont("Mono", SZ[0]//10, bold=True)
        missile_score_sur = bf.render("{:>3}".format(5), False, settings.COLOUR).convert_alpha() #Magic number straight from scoring rules, hehe
        m_sur = bf.render(str(self.multiplier), False, settings.COLOUR).convert_alpha()
        n_sur = bf.render(str(self.missiles), False, settings.COLOUR).convert_alpha()

        missile_line_sur = pg.Surface( (c_sur.get_width()+3*x_sur.get_width()+n_sur.get_width() + missile_score_sur.get_width() + m_sur.get_width(), bf.get_linesize()) )
        missile_line_sur.fill(constants.PUREBLACK)
        missile_line_sur.set_colorkey(constants.PUREBLACK)

        def gh(sur):
            return bf.get_linesize()//2 - sur.get_height()//2
        def gw(sur_list):
            return sum([sur.get_width() for sur in sur_list])
        missile_line_sur.blit(c_sur, (0, gh(c_sur)))
        missile_line_sur.blit(x_sur, (gw([c_sur]), gh(x_sur)))
        missile_line_sur.blit(n_sur, (gw([c_sur, x_sur]), gh(n_sur)))
        missile_line_sur.blit(x_sur, (gw([c_sur, x_sur, n_sur]), gh(x_sur)))
        missile_line_sur.blit(missile_score_sur, (gw([c_sur, x_sur, n_sur, x_sur]), gh(missile_score_sur)))
        missile_line_sur.blit(x_sur, (gw([c_sur, x_sur, n_sur, x_sur, missile_score_sur]), gh(x_sur)))
        missile_line_sur.blit(m_sur, (gw([c_sur, x_sur, n_sur, x_sur, missile_score_sur, x_sur]), gh(m_sur)))

        return missile_line_sur.convert_alpha()

    def draw(self, screen):
        super().draw(screen)
        screen.blit(self.c_sur, (SZ[0]//2 - self.c_sur.get_width()//2, SZ[1]//3 - self.c_sur.get_height()//2))
        screen.blit(self.m_sur, (SZ[0]//2 - self.m_sur.get_width()//2, SZ[1]//3 + self.c_sur.get_height()*1.5 - self.m_sur.get_height()//2))
            
        lh = SZ[1]//3 + self.c_sur.get_height()*2
        lw = self.m_sur.get_width()//2
        pg.draw.line(screen, settings.COLOUR, (SZ[0]//2 - lw, lh), (SZ[0]//2 + lw, lh), 4)
        dtools.dtext(screen, "= {}".format(self.score_diff), (SZ[0]//2, lh + 40))








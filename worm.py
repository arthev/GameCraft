import pygame
import colour_constants

SCREEN_SIZE = (640, 480)
HALF_WIDTH = SCREEN_SIZE[0]//2
HALF_HEIGHT = SCREEN_SIZE[1]//2

COLOUR = colour_constants.AMBER
BLACK = colour_constants.DISPLAYBLACK
PUREBLACK = colour_constants.PUREBLACK #Easy access for colorkey.
SETTINGS_PATH = "config_worm.cfg"

MENU_DWINDLE = 0.6

up_button = pygame.K_UP
left_button = pygame.K_LEFT
down_button = pygame.K_DOWN
right_button = pygame.K_RIGHT

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
global_font = pygame.font.SysFont("Mono", SCREEN_SIZE[0]//20, bold=True)

scene_stack = []

def ef(): 
    print("Yeah...")

class Scene:
    def __init__(self): pass
    def update(self): pass
    def draw(self): pass


class Menu_Scene(Scene):
    def __init__(self, options, keybindings = None):
        if keybindings == None:
            self.keybindings = [{up_button: self.select_up},
                                {down_button: self.select_down},
                                {pygame.K_RETURN: self.call_selected},
                                {pygame.K_ESCAPE: exit}]
        else: self.keybindings = keybindings
        self.selection = 0
        self.options = options
        for e in self.options:
            if e["surface"] == None:
                e["surface"] = global_font.render(e["text"], False, COLOUR).convert_alpha()

    def get_select_up(self) -> int:
        if self.selection == 0: return len(self.options) - 1
        else: return self.selection - 1
    def get_select_down(self) -> int:
        if self.selection == len(self.options) - 1: return 0
        else: return self.selection + 1
    def select_up(self):
        self.selection = self.get_select_up()
    def select_down(self):
        self.selection = self.get_select_down()

    def call_selected(self):
        self.options[self.selection]["func"]()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.constants.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                for binding in self.keybindings:
                    if event.key in binding:
                        binding[event.key]()

    def draw(self):
        screen.fill(BLACK)

        cur_sel = self.options[self.selection]["surface"]
        screen.blit(cur_sel, (HALF_WIDTH - cur_sel.get_width()//2,
                              HALF_HEIGHT - cur_sel.get_height()//2))
        
        abo_sel_o = self.options[self.get_select_up()]["surface"]
        abo_sel = pygame.transform.smoothscale(abo_sel_o, (round(abo_sel_o.get_width()*MENU_DWINDLE),
                                                    (round(abo_sel_o.get_height()*MENU_DWINDLE))))
        screen.blit(abo_sel, (HALF_WIDTH - abo_sel.get_width()//2,
                             HALF_HEIGHT - cur_sel.get_height() * 1.5))

        bel_sel_o = self.options[self.get_select_down()]["surface"]
        bel_sel = pygame.transform.smoothscale(bel_sel_o, (round(bel_sel_o.get_width()*MENU_DWINDLE),
                                                    (round(bel_sel_o.get_height()*MENU_DWINDLE))))
        screen.blit(bel_sel, (HALF_WIDTH - bel_sel.get_width()//2,
                              HALF_HEIGHT + cur_sel.get_height() * 1.5 - bel_sel.get_height()))

        pygame.display.update()



class Settings_Menu(Menu_Scene):
    def save_settings(self):
        #TODO: Actual saving lol
        scene_stack.pop()

    def __init__(self):
        options = [{"text":"Dummy", "func": ef, "surface":None},
                   {"text":"Save Settings", "func": self.save_settings, "surface": None}]
        Menu_Scene.__init__(self, options)





class Main_Menu(Menu_Scene):
    def goto_settings(self):
        scene_stack.append(Settings_Menu())

    def __init__(self):

        #Leave surface: None for those without any extras.
        options = [{"text":"Play",       "func": ef, "surface": None},
                   {"text":"High Score", "func": ef, "surface": None},
                   {"text":"Settings",   "func": self.goto_settings, "surface": None},
                   {"text":"Exit",       "func": exit, "surface": None}]

        Menu_Scene.__init__(self, options)




def main_loop():
    while True:
        try:
            current_scene = scene_stack[-1]
            current_scene.update()
            current_scene.draw()
        except IndexError:
            #Scene_stack empty; time to quit.
            exit()

if __name__ == '__main__':
    #load_settings()
    #scene_stack.append(Splash_Screen())
    scene_stack.append(Main_Menu())
    main_loop()


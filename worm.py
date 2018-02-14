import pygame
import random
import colour_constants
from enum import Enum
from collections import deque

SCREEN_SIZE = (640, 480)
HALF_WIDTH = SCREEN_SIZE[0]//2
HALF_HEIGHT = SCREEN_SIZE[1]//2
BLOCKSIZE = 32
MAX_FPS = 10

COLOUR = colour_constants.AMBER
BLACK = colour_constants.DISPLAYBLACK
PUREBLACK = colour_constants.PUREBLACK #Easy access for colorkey.
SETTINGS_PATH = "config_worm.cfg"

MENU_DWINDLE = 0.6

up_button = pygame.K_UP
left_button = pygame.K_LEFT
down_button = pygame.K_DOWN
right_button = pygame.K_RIGHT
pause_button = pygame.K_p

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
global_font = pygame.font.SysFont("Mono", SCREEN_SIZE[0]//20, bold=True)

scene_stack = []
d = Enum('Direction', 'DOWN RIGHT UP LEFT')

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
    def start_game(self):
        scene_stack.append(Game_Scene())

    def __init__(self):

        #Leave surface: None for those without any extras.
        options = [{"text":"Play",       "func": self.start_game, "surface": None},
                   {"text":"High Score", "func": ef, "surface": None},
                   {"text":"Settings",   "func": self.goto_settings, "surface": None},
                   {"text":"Exit",       "func": exit, "surface": None}]

        Menu_Scene.__init__(self, options)

class Pause(Scene):
    def pause_over(self):
        scene_stack.pop()

    def __init__(self):
        self.background = pygame.Surface.copy(screen)
    
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.constants.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pause_button or event.key == pygame.K_RETURN:
                    self.pause_over()
                elif event.key == pygame.K_ESCAPE:
                    exit()
    
    def draw(self):  
        overlay = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
        pygame.draw.rect(overlay, (0, 0, 0, 200), (0, 0, SCREEN_SIZE[0], SCREEN_SIZE[1]))
        text = global_font.render("Paused", False, COLOUR).convert_alpha()
        screen.blit(self.background, (0, 0))
        screen.blit(overlay, (0, 0))
        screen.blit(text, (HALF_WIDTH - text.get_width()//2,
                           HALF_HEIGHT- text.get_height()//2))




class Game_Scene(Scene):
    def goto_pause(self):
        scene_stack.append(Pause())

    def get_apple_position(self):
        pos = random.randint(0, self.width), random.randint(0, self.height)
        for segment in self.snake:
            if segment == pos:
                return self.get_apple_position()
        return pos


    def __init__(self):
        self.width = SCREEN_SIZE[0]//BLOCKSIZE - 1 #0-indexed
        self.height = SCREEN_SIZE[1]//BLOCKSIZE - 1
        middle_w = self.width//2
        middle_h = self.height//2
        
        self.snake = deque([(middle_w, middle_h),
                            (middle_w, middle_h - 1),
                            (middle_w, middle_h - 2)])
        self.v = d.DOWN #This is the direction variable.
        self.apple = self.get_apple_position()

        BZS = BLOCKSIZE//16
        BZE = BLOCKSIZE//8
        BZF = BLOCKSIZE//4
        block_surface = pygame.Surface( (BLOCKSIZE, BLOCKSIZE) )
        block_surface.fill(BLACK)
        pygame.draw.rect(block_surface, COLOUR, (BZS, BZS, BLOCKSIZE - BZS, BLOCKSIZE - BZS))
        self.seg_sur = block_surface.convert()
        #Now for the head...
        pygame.draw.circle(block_surface, BLACK, (BZF, BLOCKSIZE - BZF), BZE)
        pygame.draw.circle(block_surface, BLACK, (BLOCKSIZE - BZF, BLOCKSIZE - BZF), BZE)
        self.head_sur_d = block_surface.convert()
        pygame.draw.circle(block_surface, COLOUR, (BLOCKSIZE - BZF, BLOCKSIZE - BZF), BZE)
        pygame.draw.circle(block_surface, BLACK, (BZF, BZF), BZE)
        self.head_sur_l = block_surface.convert()
        pygame.draw.circle(block_surface, COLOUR, (BZF, BLOCKSIZE - BZF), BZE)
        pygame.draw.circle(block_surface, BLACK, (BLOCKSIZE - BZF, BZF), BZE)
        self.head_sur_u = block_surface.convert()
        pygame.draw.circle(block_surface, COLOUR, (BZF, BZF), BZE)
        pygame.draw.circle(block_surface, BLACK, (BLOCKSIZE - BZF, BLOCKSIZE - BZF), BZE)
        self.head_sur_r = block_surface.convert()

        #And now the apple...
        self.apple_sur = pygame.Surface( (BLOCKSIZE, BLOCKSIZE) )
        self.apple_sur.fill(BLACK)
        pygame.draw.circle(self.apple_sur, COLOUR, (BLOCKSIZE//2, BLOCKSIZE//2), BLOCKSIZE//2, BLOCKSIZE//8)
        pygame.draw.circle(self.apple_sur, COLOUR, (BLOCKSIZE//2, BLOCKSIZE//2), BLOCKSIZE//4, BLOCKSIZE//4)
        self.apple_sur.convert()
        

        self.clock = pygame.time.Clock()
        

    def update(self):
        self.clock.tick(MAX_FPS)
        
        prev_v = self.v
        for event in pygame.event.get():
            if event.type == pygame.constants.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                elif event.key == up_button:
                    if not prev_v == d.DOWN: self.v = d.UP
                elif event.key == down_button:
                    if not prev_v == d.UP: self.v = d.DOWN
                elif event.key == left_button:
                    if not prev_v == d.RIGHT: self.v = d.LEFT
                elif event.key == right_button:
                    if not prev_v == d.LEFT: self.v = d.RIGHT
                elif event.key == pause_button:
                    self.goto_pause()
        
        head_x, head_y = self.snake[0]
        if self.v == d.DOWN: dy = 1
        elif self.v == d.UP: dy = -1
        else: dy = 0
        if self.v == d.RIGHT: dx = 1
        elif self.v == d.LEFT: dx = -1
        else: dx = 0
        if head_x + dx > self.width: dx = -head_x
        elif head_x + dx < 0: dx = self.width
        if head_y + dy > self.height: dy = -head_y
        elif head_y + dy < 0: dy = self.height

        self.snake.appendleft((head_x + dx, head_y + dy))

        if self.apple != self.snake[0]:
            self.snake.pop()
        else:
            self.apple = self.get_apple_position()

        for i, s in enumerate(self.snake):
            if s == self.snake[0] and i != 0:
                self.game_over()

    def game_over(self):
        print("Well, you lost mate...")
        scene_stack.pop()

    def draw(self):
        screen.fill(BLACK)
        for segment in self.snake:
            x, y = segment
            screen.blit(self.seg_sur, (x * BLOCKSIZE, y * BLOCKSIZE))
        #Turns out deques can't be sliced. But I just want to draw the head itself differently anyhow. Well, I can just draw it over the result from the loop above...
        x, y = self.snake[0]
        if self.v == d.DOWN: screen.blit(self.head_sur_d, (x * BLOCKSIZE, y * BLOCKSIZE))
        elif self.v == d.RIGHT: screen.blit(self.head_sur_r, (x * BLOCKSIZE, y * BLOCKSIZE))
        elif self.v == d.UP: screen.blit(self.head_sur_u, (x * BLOCKSIZE, y * BLOCKSIZE))
        elif self.v == d.LEFT: screen.blit(self.head_sur_l, (x * BLOCKSIZE, y * BLOCKSIZE))
        x, y = self.apple
        screen.blit(self.apple_sur, (x * BLOCKSIZE, y * BLOCKSIZE))


def main_loop():
    while True:
        try:
            current_scene = scene_stack[-1]
            current_scene.update()
            current_scene.draw()
            pygame.display.update()
        except IndexError:
            #Scene_stack empty; time to quit.
            exit()

if __name__ == '__main__':
    #load_settings()
    #scene_stack.append(Splash_Screen())
    scene_stack.append(Main_Menu())
    main_loop()

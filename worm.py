import pygame
import random
import colour_constants
import json
from enum import Enum
from collections import deque
from pathlib import Path

SCREEN_SIZE = (640, 480)
HALF_WIDTH = SCREEN_SIZE[0]//2
HALF_HEIGHT = SCREEN_SIZE[1]//2
BLOCKSIZE = 32

COLOUR = colour_constants.AMBER
BLACK = colour_constants.DISPLAYBLACK
PUREBLACK = colour_constants.PUREBLACK #Easy access for colorkey.
SETTINGS_PATH = Path("data", "config_worm.cfg")

MENU_DWINDLE = 0.6
APPLE_SCORE = 10

up_button = pygame.K_UP
left_button = pygame.K_LEFT
down_button = pygame.K_DOWN
right_button = pygame.K_RIGHT
pause_button = pygame.K_p
fps = 10

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
    #Leave surface: None for those without any extras, in the options.
    def __init__(self, options, keybindings = None):
        if keybindings == None:
            self.keybindings = [{up_button: self.select_up},
                                {down_button: self.select_down},
                                {right_button: self.select_right},
                                {left_button: self.select_left},
                                {pygame.K_RETURN: self.call_selected},
                                {pygame.K_ESCAPE: exit}]
        else: self.keybindings = keybindings
        self.selection = 0
        self.options = options

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

    def select_right(self):
        cur = self.options[self.selection]
        if "right" in cur: cur["right"]()

    def select_left(self):
        cur = self.options[self.selection]
        if "left" in cur: cur["left"]()

    def call_selected(self):
        selected = self.options[self.selection]
        if "var" in selected:
            selected["func"](selected)
        else:
            self.options[self.selection]["func"]()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.constants.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                for binding in self.keybindings:
                    if event.key in binding:
                        binding[event.key]()

    def get_base_surface(self, specifier):
        if specifier["surface"] == None:
            return global_font.render(specifier["text"], False, COLOUR).convert_alpha()
        elif "var" in specifier:
            return specifier["surface"](specifier)
        else:
            return specifier["surface"]()

    def draw(self):
        screen.fill(BLACK)

        cur_sel = self.get_base_surface(self.options[self.selection])
        screen.blit(cur_sel, (HALF_WIDTH - cur_sel.get_width()//2,
                              HALF_HEIGHT - cur_sel.get_height()//2))
        
        abo_sel_o = self.get_base_surface(self.options[self.get_select_up()])
        abo_sel = pygame.transform.smoothscale(abo_sel_o, (round(abo_sel_o.get_width()*MENU_DWINDLE),
                                                    (round(abo_sel_o.get_height()*MENU_DWINDLE))))
        screen.blit(abo_sel, (HALF_WIDTH - abo_sel.get_width()//2,
                             HALF_HEIGHT - cur_sel.get_height() * 1.5))

        bel_sel_o = self.get_base_surface(self.options[self.get_select_down()])
        bel_sel = pygame.transform.smoothscale(bel_sel_o, (round(bel_sel_o.get_width()*MENU_DWINDLE),
                                                    (round(bel_sel_o.get_height()*MENU_DWINDLE))))
        screen.blit(bel_sel, (HALF_WIDTH - bel_sel.get_width()//2,
                              HALF_HEIGHT + cur_sel.get_height() * 1.5 - bel_sel.get_height()))

class Settings_Menu(Menu_Scene):
    def save_settings(self):
        current_settings = {'COLOUR':COLOUR,
                            'fps':fps,
                            'up_button':up_button,
                            'down_button':down_button,
                            'left_button':left_button,
                            'right_button':right_button,
                            'pause_button':pause_button}
        with open(str(SETTINGS_PATH), 'w') as settings_file:
            json.dump(current_settings, settings_file)
        scene_stack.pop()
        scene_stack.pop()
        menu = Main_Menu()
        menu.selection = 3
        scene_stack.append(menu)

    def set_key(self, specifier):
        scene_stack.append(Set_Key(specifier))

    def arrow_surface(self, msg):
        text = global_font.render(msg, False, COLOUR).convert_alpha()

        h = text.get_height()*0.75//1
        arrows = pygame.Surface((h, h))
        arrows.fill(BLACK)
        pygame.draw.polygon(arrows, COLOUR,
                ( (0, h//2), (h//2 - h//8, h//4), (h//2 - h//8, 3*h//4) ) )
        pygame.draw.polygon(arrows, COLOUR,
                ( (h, h//2), (h//2 + h//8, h//4), (h//2 + h//8, 3*h//4) ) )
        c_sur = pygame.Surface((text.get_width() + arrows.get_width() + h//4,
                                 text.get_height()))
        c_sur.fill(BLACK)
        c_sur.blit(arrows, (0, h//8))
        c_sur.blit(text, (arrows.get_width() + h//4, 0))
        c_sur.convert_alpha()
        return c_sur

    def colour_surface(self):
        return self.arrow_surface("Colour")
    def colour_right(self):
        global COLOUR
        if self.colour_selection == len(self.colour_options) - 1:
            self.colour_selection = 0
        else: self.colour_selection += 1
        COLOUR = self.colour_options[self.colour_selection]
    def colour_left(self):
        global COLOUR
        if self.colour_selection == 0:
            self.colour_selection = len(self.colour_options) - 1
        else: self.colour_selection -= 1
        COLOUR = self.colour_options[self.colour_selection]

    def speed_surface(self):
        return self.arrow_surface("Difficulty: " + str(fps))
    def speed_right(self):
        global fps
        fps += 1
    def speed_left(self):
        global fps
        fps = max(1, fps - 1)

    def key_surface(self, specifier):
        key_name = pygame.key.name(globals()[specifier["var"]])
        return global_font.render(specifier["text"] + key_name, False, COLOUR).convert_alpha()

    def __init__(self):
        self.colour_options = [colour_constants.AMBER,
                               colour_constants.LTAMBER,
                               colour_constants.GREEN1,
                               colour_constants.APPLE1,
                               colour_constants.GREEN2,
                               colour_constants.APPLE2,
                               colour_constants.GREEN3]
        self.colour_selection = 0
        for i, colour in enumerate(self.colour_options):
            if colour == COLOUR:
                self.colour_selection = i
        options = [{"text":"Colour", "func": ef, "surface":self.colour_surface,
                       "right":self.colour_right, "left":self.colour_left},
                   {"text":"Speed", "func": ef, "surface":self.speed_surface,
                       "right":self.speed_right, "left":self.speed_left},
                   {"text":"Up:", "func": self.set_key, "var":"up_button",
                       "surface":self.key_surface},
                   {"text":"Down:", "func": self.set_key, "var":"down_button",
                       "surface":self.key_surface},
                   {"text":"Left:", "func": self.set_key, "var":"left_button",
                       "surface":self.key_surface},
                   {"text":"Right:", "func": self.set_key, "var":"right_button",
                       "surface":self.key_surface},
                   {"text":"Pause:", "func": self.set_key, "var":"pause_button",
                       "surface":self.key_surface},
                   {"text":"Save Settings", "func": self.save_settings, "surface": None}]
        Menu_Scene.__init__(self, options)

class Main_Menu(Menu_Scene):
    def goto_settings(self):
        scene_stack.append(Settings_Menu())
    def start_game(self):
        scene_stack.append(Game_Scene())

    def __init__(self):
        options = [{"text":"Play",       "func": self.start_game, "surface": None},
                   {"text":"High Score", "func": ef, "surface": None},
                   {"text":"Settings",   "func": self.goto_settings, "surface": None},
                   {"text":"Exit",       "func": exit, "surface": None}]
        #Create a little snaky drawing to spruce up
        bz = BLOCKSIZE//2
        bzz = max(bz//16, 1)
        bzf = bz//4
        bze = bz//8
        self.spruce = pygame.Surface((bz*8, bz*8))
        self.spruce.fill(BLACK)
        block_sur = pygame.Surface((bz, bz))
        block_sur.fill(BLACK)
        pygame.draw.rect(block_sur, COLOUR,
                (bzz, bzz, bz - bzz, bz - bzz))
        block_sur = block_sur.convert()
        for t in [(2,4),(2,5),(2,6),(2,7),
                  (3,7),
                  (4,7),(5,7),
                  (5,6),(5,5),(5,4),(5,3)]:
            x, y = t
            self.spruce.blit(block_sur, (x*bz, y*bz))
        head_sur = block_sur
        pygame.draw.circle(head_sur, BLACK,
                (bzf, bzf), bze)
        pygame.draw.circle(head_sur, BLACK,
                (bz - bzf, bzf), bze)
        head_sur = head_sur.convert()
        x, y = (5, 2)
        self.spruce.blit(head_sur, (x*bz, y*bz))

        Menu_Scene.__init__(self, options)

    def draw(self):
        Menu_Scene.draw(self)
        screen.blit(self.spruce,
                (HALF_WIDTH - self.spruce.get_width()//2,
                self.spruce.get_height()//6))

class Overlay_Scene(Scene):
    def cont(self):
        scene_stack.pop()

    def __init__(self):
        self.background = pygame.Surface.copy(screen)
        self.overlay = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
        pygame.draw.rect(self.overlay, (0, 0, 0, 200), (0, 0, SCREEN_SIZE[0], SCREEN_SIZE[1]))

    def draw(self):
        screen.blit(self.background, (0, 0))
        screen.blit(self.overlay, (0, 0))

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.constants.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pause_button or event.key == pygame.K_RETURN:
                    self.cont()
                elif event.key == pygame.K_ESCAPE:
                    exit()

class Set_Key(Overlay_Scene):
    def cont(self, key):
        globals()[self.specified["var"]] = key
        scene_stack.pop()

    def __init__(self, specified):
        self.specified = specified
        Overlay_Scene.__init__(self)

    def draw(self):
        Overlay_Scene.draw(self)
        text = global_font.render("Press desired key...", False, COLOUR).convert_alpha()
        screen.blit(text, (HALF_WIDTH - text.get_width()//2,
                           HALF_HEIGHT- text.get_height()//2))

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.constants.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key != pause_button and event.key != pygame.K_RETURN:
                    self.cont(event.key)

class Pause(Overlay_Scene):
    def draw(self):  
        Overlay_Scene.draw(self)
        text = global_font.render("Paused", False, COLOUR).convert_alpha()
        screen.blit(text, (HALF_WIDTH - text.get_width()//2,
                           HALF_HEIGHT- text.get_height()//2))

class Game_Over(Overlay_Scene):
    def cont(self):
        scene_stack.pop()
        scene_stack.pop()
        #TODO: Append the high score scene...
        #scene_stack.append(High_Score_Entry(self.score))
    def __init__(self, score):
        self.score = score
        Overlay_Scene.__init__(self)
    def draw(self):
        Overlay_Scene.draw(self)
        text = global_font.render("Game Over", False, COLOUR)
        screen.blit(text, (HALF_WIDTH - text.get_width()//2,
                           HALF_HEIGHT-text.get_height()//2))

class Board_Won(Overlay_Scene):
    def __init__(self, score):
        self.score = score
        Overlay_Scene.__init__(self)

    def draw(self):
        Overlay_Scene.draw(self)
        text = global_font.render("Board Cleared! Well done!", False, COLOUR).convert_alpha()
        screen.blit(text, (HALF_WIDTH - text.get_width()//2,
                           HALF_HEIGHT-text.get_height()//2 - global_font.get_linesize()//2))
        infotext = global_font.render("Press Return or Pause to continue.", False, COLOUR).convert_alpha()
        infotext = pygame.transform.scale(infotext, (round(infotext.get_width()*MENU_DWINDLE),
                                                     round(infotext.get_height()*MENU_DWINDLE)))
        screen.blit(infotext, (HALF_WIDTH - infotext.get_width()//2,
                               HALF_HEIGHT-infotext.get_height()//2 + global_font.get_linesize()//2))

class Game_Scene(Scene):
    def goto_pause(self):
        scene_stack.append(Pause())

    def get_apple_position(self):
        pos = random.randint(0, self.width), random.randint(0, self.height)
        for segment in self.snake:
            if segment == pos:
                return self.get_apple_position()
        return pos

    def reset_board(self):
        middle_w = self.width//2
        middle_h = self.height//2
        self.snake = deque([(middle_w, middle_h),
                            (middle_w, middle_h - 1),
                            (middle_w, middle_h - 2)])
        self.v = d.DOWN #This is the direction variable.
        self.apple = self.get_apple_position()

    def __init__(self):
        self.width = SCREEN_SIZE[0]//BLOCKSIZE - 1 #0-indexed
        self.height = SCREEN_SIZE[1]//BLOCKSIZE - 1

        self.reset_board() #Sets the self.snake, self.v and self.apple members
        self.score = 0
        self.speed = fps

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
        self.clock.tick(self.speed)
        
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
                elif event.key == pygame.K_SPACE:
                    self.board_won()
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
            if len(self.snake) == (self.width+1)*(self.height+1):
                self.board_won()
            self.apple = self.get_apple_position()
            self.score += self.speed*(APPLE_SCORE + len(self.snake))//20
            print("New score:", self.score)

        for i, s in enumerate(self.snake):
            if s == self.snake[0] and i != 0:
                self.game_over()

    def board_won(self):
        scene_stack.append(Board_Won(self.score))
        self.reset_board()
        self.speed += 3

    def game_over(self):
        N = 6
        if N % 2 == 0: N += 1
        for i in range(N):
            self.clock.tick(N//2)
            if i % 2 == 0: self.draw()
            else: screen.fill(BLACK)
            pygame.display.update()
        self.clock.tick(N//2)
        scene_stack.append(Game_Over(self.score))

    def draw(self):
        screen.fill(BLACK)
        for segment in self.snake:
            x, y = segment
            screen.blit(self.seg_sur, (x * BLOCKSIZE, y * BLOCKSIZE))
        #Turns out deques can't be sliced. But I just want to draw the head differently.
        #Well, I can just draw it over the result from the loop above, hehe.
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

def load_settings():
    if SETTINGS_PATH.is_file():
        with open(str(SETTINGS_PATH), 'r') as settings_file:
            settings = json.load(settings_file)
            for item in settings:
                globals()[item] = settings[item]
    else:
        scene_stack.append(Settings_Menu())
        scene_stack[-1].save_settings() #This pops the save_settings too.

if __name__ == '__main__':
    load_settings()
    #scene_stack.append(Splash_Screen())
    scene_stack.append(Main_Menu())
    #scene_stack.append(Game_Scene())
    main_loop()

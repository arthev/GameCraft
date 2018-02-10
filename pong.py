import pygame
import random
import colour_constants
import time
import json
import math
from pathlib import Path

SCREEN_SIZE = (640, 480)
BALL_DIAMETER = 32
MAX_FPS = 60
PADDLE_SIZE = (16, 64)
PADDLE_VEL = 10
HORIZONTAL_BAR = (SCREEN_SIZE[0], PADDLE_SIZE[0])
RECENT_HIT_RESET = 20
BLACK     = colour_constants.DISPLAYBLACK 
PUREBLACK = colour_constants.PUREBLACK #Easy access for colorkeying
SETTINGS_PATH = "config_pong.cfg"

COLOUR    = colour_constants.APPLE2
player_one_up = pygame.K_q
player_one_down = pygame.K_a
player_two_up = pygame.K_o
player_two_down = pygame.K_l
points_per_game = 5

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
font = pygame.font.SysFont("Mono", 32)

class Play_Background:
    def __init__(self):
        self.surface = pygame.Surface(SCREEN_SIZE)
        self.surface.fill(BLACK)
        self.surface = self.surface.convert()
        pygame.draw.rect(self.surface, COLOUR, (0, 0, HORIZONTAL_BAR[0], HORIZONTAL_BAR[1]))
        pygame.draw.rect(self.surface, COLOUR, (0, SCREEN_SIZE[1] - HORIZONTAL_BAR[1], HORIZONTAL_BAR[0], HORIZONTAL_BAR[1]))
        pygame.draw.line(self.surface, COLOUR, (SCREEN_SIZE[0]//2, 0), (SCREEN_SIZE[0]//2, SCREEN_SIZE[1]))

    def draw(self) -> None:
        screen.blit( self.surface, (0, 0) )

class vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)
    
    def normalize(self):
        magnitude = self.get_magnitude()
        self.x /= magnitude
        self.y /= magnitude

    def __add__(self, rhs):
        return vector2(self.x + rhs.x, self.y + rhs.y)
    
    def __mul__(self, scalar):
        return vector2(self.x * scalar, self.y * scalar)


class Paddle:
    def __init__(self, side, player, up_button=None, down_button=None):
        if side == "left":
            self.pos = vector2(SCREEN_SIZE[0]//40, SCREEN_SIZE[1]//2 - PADDLE_SIZE[1]//2)
        elif side == "right":
            self.pos = vector2(SCREEN_SIZE[0] - PADDLE_SIZE[0] - SCREEN_SIZE[0]//40, SCREEN_SIZE[1]//2 - PADDLE_SIZE[1]//2)
        else:
            raise ValueError("Illegal 'side' argument sent to Paddle.__init__:", side)
        if player and (up_button == None or up_button == None):
            raise ValueError("Illegal combination of player and buttons sent to Paddle.__init__. None buttons make no sense for player == True")
        self.side = side
        self.player = player
        self.up_button = up_button
        self.down_button = down_button
        self.vel = vector2(0, 0) #No initial movement.
        self.surface = pygame.Surface( (PADDLE_SIZE[0], PADDLE_SIZE[1]) )
        self.surface.fill(COLOUR)
        self.surface = self.surface.convert()
        self.score = 0

    def move(self, time_passed) -> None:
        #Accelerate
        if self.player:
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[self.up_button]:
                self.vel.y -= PADDLE_VEL
            elif pressed_keys[self.down_button]:
                self.vel.y += PADDLE_VEL
            else:
                self.vel.y -= self.vel.y / (MAX_FPS * 1.3) #Found experimentally
        else:
            #TODO: Handle AI
            print("No AI implemented yet.")
            pass
        #Move
        self.pos.y += self.vel.y * time_passed
        if self.pos.y < HORIZONTAL_BAR[1] or self.pos.y + PADDLE_SIZE[1] > SCREEN_SIZE[1] - HORIZONTAL_BAR[1]:
            self.vel.y *= -0.75
            if self.pos.y < HORIZONTAL_BAR[1]:
                self.pos.y = HORIZONTAL_BAR[1]
            else:
                self.pos.y = SCREEN_SIZE[1] - PADDLE_SIZE[1] - HORIZONTAL_BAR[1]

    def draw(self) -> None:
        screen.blit(self.surface, (self.pos.x, self.pos.y))

class Ball:
    def reset(self) -> None:
        self.recent_hit = 0
        self.pos = vector2(SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2)
        self.vel = vector2(SCREEN_SIZE[0] * random.random(), SCREEN_SIZE[1] * random.random())

    def __init__(self):
        self.pos = None
        self.vel = None
        self.surface = pygame.Surface( (BALL_DIAMETER, BALL_DIAMETER) )
        self.surface.set_colorkey(PUREBLACK)
        pygame.draw.circle( self.surface, COLOUR, (BALL_DIAMETER//2, BALL_DIAMETER//2), BALL_DIAMETER//2)
        self.surface = self.surface.convert_alpha()
        self.recent_hit = None
        self.reset()

    def horizontal_bar_check_and_adjustment(self) -> None:
        if self.pos.y < HORIZONTAL_BAR[1] or self.pos.y + BALL_DIAMETER > SCREEN_SIZE[1] - HORIZONTAL_BAR[1]:
            self.vel.y *= -1
            if self.pos.y < HORIZONTAL_BAR[1]:
                self.pos.y = HORIZONTAL_BAR[1]
            else:
                self.pos.y = SCREEN_SIZE[1] - BALL_DIAMETER - HORIZONTAL_BAR[1]

    def score_check(self) -> str: #Can also return None!
        if self.pos.x + BALL_DIAMETER < 0:
            return "right"
        elif self.pos.x > SCREEN_SIZE[0]:
            return "left"
        else:
            return None

    def simple_collision_check(self, paddles) -> Paddle: #Can also return None!
        left = paddles[0]
        right = paddles[1]
        if self.recent_hit > 0:
            return None
        if self.pos.x + BALL_DIAMETER < right.pos.x and self.pos.x > left.pos.x + PADDLE_SIZE[0]:
            return None
        #If we progress below here, a hit might happen... since the ball isn't *between* the paddles!
        if self.pos.x + BALL_DIAMETER > right.pos.x:
            #Ball might have hit the right paddle.
            if self.pos.y > right.pos.y + PADDLE_SIZE[1]:
                return None
            elif self.pos.y + BALL_DIAMETER < right.pos.y:
                return None
            else:
                return right
        else:
            #Ball might have hit the left paddle.
            if self.pos.y > left.pos.y + PADDLE_SIZE[1]:
                return None
            elif self.pos.y + BALL_DIAMETER < left.pos.y:
                return None
            else:
                return left

    def collision_handling(self, paddle) -> None:
        steps = PADDLE_SIZE[1]//2 + BALL_DIAMETER//2
        extreme = 1.12 #arcsin(0.9) = 1.12
        hit = self.pos.y + BALL_DIAMETER//2 - (paddle.pos.y + PADDLE_SIZE[1]//2)
        w = extreme/steps*hit
        newVec = 0 #This is a unit vector, hehe.
        if paddle.side == "left": newVec = vector2(-math.cos(w), -math.sin(w))
        else: newVec = vector2(math.cos(w), -math.sin(w))
        magnitude = self.vel.get_magnitude() * 1.05 * -1
        self.vel.normalize()
        newVec = newVec + self.vel #The two vectors can be scalar multiplied by some percentage for different admixtures.
        newVec.normalize()
        newVec = newVec * magnitude
        self.vel = newVec






    def move(self, time_passed, paddles) -> None:
        self.pos.x += self.vel.x * time_passed
        self.pos.y += self.vel.y * time_passed
        if self.recent_hit > 0: self.recent_hit -= 1
        self.horizontal_bar_check_and_adjustment()
        quick_collision = self.simple_collision_check(paddles) #quick_collision will contain a paddle - or None.
        if quick_collision: 
            self.recent_hit = RECENT_HIT_RESET
            self.collision_handling(quick_collision)

    def draw(self) -> None:
        screen.blit(self.surface, (self.pos.x, self.pos.y))

class Scoredrawer:
    def __init__(self):
        self.left = 0
        self.right = 0

    def draw(self, left, right): #Idea for improved performance: Check whether there's a change to a score and then only rendering if so.
        left_text  = font.render(str(left),  False, COLOUR).convert_alpha()
        right_text = font.render(str(right), False, COLOUR).convert_alpha()
        y_offset = HORIZONTAL_BAR[1] * 1.5
        screen.blit(left_text,  (SCREEN_SIZE[0]//2 - 32 - left_text.get_width(),  y_offset))
        screen.blit(right_text, (SCREEN_SIZE[0]//2 + 32, y_offset))

def display_winner(winner) -> None:
    winner_text = font.render( winner.capitalize() + " has won!", False, COLOUR).convert_alpha()
    screen.blit(winner_text, (SCREEN_SIZE[0]//2 - winner_text.get_width()//2,
                              SCREEN_SIZE[1]//2 - winner_text.get_height()//2))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.constants.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                elif event.key == pygame.K_RETURN:
                    return

def play(win_score: int, two_player_mode: bool) -> str: #returns 'left' or 'right' depending on which player won
    clock = pygame.time.Clock()

    background = Play_Background()
    scoredrawer = Scoredrawer()
    ball = Ball()
    paddle1 = Paddle(side="left", player=True, up_button=player_one_up, down_button=player_one_down)
    paddle2 = Paddle(side="right", player=two_player_mode, up_button=player_two_up, down_button=player_two_down)
    paddles = [paddle1, paddle2] #Left side must go in paddles[0], right side in paddles[1].

    while True:
        for event in pygame.event.get():
            if event.type == pygame.constants.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()

        time_passed = clock.tick(MAX_FPS) / 1000.0 #time_passed is in seconds

        background.draw()

        ball.move(time_passed, paddles)
        for paddle in paddles: paddle.move(time_passed)
        
        scorer = ball.score_check() #Either "left", "right" or None
        if scorer:
            if scorer == "left":
                paddles[0].score += 1
                if paddles[0].score >= win_score:
                    display_winner(scorer)
                    return
            else:
                paddles[1].score += 1
                if paddles[1].score >= win_score:
                    display_winner(scorer)
                    return 
            ball.reset()

        scoredrawer.draw(paddles[0].score, paddles[1].score)
        ball.draw()
        for paddle in paddles: paddle.draw()
        pygame.display.update()

def display_intro() -> None:
    display_font = pygame.font.SysFont("mono", SCREEN_SIZE[0]//6)
    display_text = display_font.render("PongyPong", False, COLOUR, BLACK).convert()
    display_font2 = pygame.font.SysFont("mono", SCREEN_SIZE[0]//18)
    display_text2 = display_font2.render("by: Arthur", False, COLOUR, BLACK).convert()
    for i in range(256):
        screen.fill(BLACK)
        display_text.set_alpha(i)
        screen.blit(display_text, (SCREEN_SIZE[0]//2 - display_text.get_width()//2,
                                   SCREEN_SIZE[1]//2 - display_text.get_height()))

        pygame.display.update()
        time.sleep(1/100)
    for i in range(256):
        display_text2.set_alpha(i)
        screen.blit(display_text2, (SCREEN_SIZE[0]//2,
                                    SCREEN_SIZE[1]//2))
        pygame.display.update()
        time.sleep(1/200)
    time.sleep(0.25)

def settings_menu() -> None:
    def save_settings(dummy):
        current_settings = {'COLOUR':COLOUR,
                            'player_one_up':player_one_up,
                            'player_one_down':player_one_down,
                            'player_two_up':player_two_up,
                            'player_two_down':player_two_down,
                            'points_per_game':points_per_game}
        with open(SETTINGS_PATH, 'w') as settings_file:
            json.dump(current_settings, settings_file)
    
    def set_key(var):
        press_message = font.render( "Press the desired key...", False, COLOUR).convert_alpha()
        screen.blit(press_message, (SCREEN_SIZE[0]//2 - press_message.get_width()//2,
                                    SCREEN_SIZE[1] - font.get_linesize() * 1.5))
        pygame.display.update()
        pygame.event.clear()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.constants.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit()
                    if event.key != pygame.K_RETURN:
                        globals()[var] = event.key
                        return

    selection = 0
    options = [{'Text': 'Points Per Game: ', 'func': lambda x: None, 'var': 'points_per_game', 'extradraw': ['arrows', 'value']},
               {'Text': 'Colour', 'func': lambda x: None, 'var': 'COLOUR', 'extradraw':'arrows'},
               {'Text': 'Player One Up: ', 'func': set_key, 'var': 'player_one_up', 'extradraw':'button'},
               {'Text': 'Player One Down: ', 'func': set_key, 'var': 'player_one_down', 'extradraw':'button'},
               {'Text': 'Player Two Up: ', 'func': set_key, 'var': 'player_two_up', 'extradraw':'button'},
               {'Text': 'Player Two Down: ', 'func': set_key, 'var':'player_two_down', 'extradraw':'button'},
               {'Text': 'Save Settings', 'func': save_settings, 'var': 'return', 'extradraw': None}]

    colour_options = [colour_constants.AMBER,
                      colour_constants.LTAMBER,
                      colour_constants.GREEN1,
                      colour_constants.APPLE1,
                      colour_constants.GREEN2,
                      colour_constants.APPLE2,
                      colour_constants.GREEN3]

    colour_selection = 0
    for i, colour in enumerate(colour_options):
        if colour == COLOUR:
            colour_selection = i

    blinker = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.constants.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                elif event.key == pygame.K_RETURN:
                    options[selection]['func'](options[selection]['var'])
                    if options[selection]['var'] == 'return': return
                elif event.key in [pygame.K_DOWN, player_one_down, player_two_down]:
                    if selection == len(options) - 1: selection = 0
                    else: selection += 1
                elif event.key in [pygame.K_UP, player_one_up, player_two_up]:
                    if selection == 0: selection = len(options) - 1
                    else: selection -= 1
                elif event.key == pygame.K_RIGHT:
                    var = options[selection]['var']
                    if var == 'COLOUR':
                        if colour_selection == len(colour_options) -1: 
                            colour_selection = 0
                        else: colour_selection += 1
                        globals()[var] = colour_options[colour_selection]
                    elif var == 'points_per_game':
                        globals()[var] += 1
                elif event.key == pygame.K_LEFT:
                    var = options[selection]['var']
                    if var == 'COLOUR':
                        if colour_selection == 0:
                            colour_selection = len(colour_options) - 1
                        else: colour_selection -= 1
                        globals()[var] = colour_options[colour_selection]
                    if var == 'points_per_game':
                        globals()[var] = max(1, points_per_game - 1)

        screen.fill(BLACK)
        DIV = 32

        for i in range(len(options)):
            if i == selection:
                blinker = not blinker
                if blinker: continue
            text = font.render(options[i]['Text'], False, COLOUR).convert_alpha()
            screen.blit(text, (SCREEN_SIZE[0]//2 - text.get_width()//2,
                               SCREEN_SIZE[1]//DIV + font.get_linesize() * 1.5 * i))
            extradraw = options[i]['extradraw']
            if extradraw == 'arrows' or (type(extradraw) == list and 'arrows' in extradraw):
                h = text.get_height() * 0.75 // 1
                arrowsurface = pygame.Surface( (h, h) )
                arrowsurface.fill(BLACK)
                pygame.draw.polygon(arrowsurface, COLOUR,
                        ( (0, h//2), (h//2 - h//8, h//4), (h//2 - h//8, 3*h//4) ) )
                pygame.draw.polygon(arrowsurface, COLOUR,
                        ( (h, h//2), (h//2 + h//8, h//4), (h//2 + h//8, 3*h//4) ) )
                arrowsurface.convert()
                screen.blit(arrowsurface, (SCREEN_SIZE[0]//2 - text.get_width()//2 - arrowsurface.get_width() - 2,
                                           SCREEN_SIZE[1]//DIV + font.get_linesize() * 1.5 * i + h//8))
            if extradraw == 'value' or (type(extradraw) == list and 'value' in extradraw):
                valuesurface = font.render( str(globals()[options[i]['var']]), False, COLOUR).convert_alpha()
                screen.blit(valuesurface, (SCREEN_SIZE[0]//2 + text.get_width()//2 + 2,
                                           SCREEN_SIZE[1]//DIV + font.get_linesize() * 1.5 * i))
            if extradraw == 'button' or (type(extradraw) == list and 'button' in extradraw):
                buttonsurface = font.render( pygame.key.name(globals()[options[i]['var']]), False, COLOUR).convert_alpha()
                screen.blit(buttonsurface, (SCREEN_SIZE[0]//2 + text.get_width()//2 + 2,
                                           SCREEN_SIZE[1]//DIV + font.get_linesize() * 1.5 * i))




        pygame.display.update()

def main_menu() -> None:
    def one_player_mode():
        play(points_per_game, False)
    def two_player_mode():
        play(points_per_game, True)

    selection = 0
    options = [{'Text': '1-Player', 'func': one_player_mode},
               {'Text': '2-Player', 'func': two_player_mode},
               {'Text': 'Settings', 'func': settings_menu},
               {'Text': 'Exit', 'func': exit}]

    blinker = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.constants.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                elif event.key == pygame.K_RETURN:
                    options[selection]['func']()
                elif event.key in [pygame.K_DOWN, player_one_down, player_two_down]:
                    if selection == len(options) - 1: selection = 0
                    else: selection += 1
                elif event.key in [pygame.K_UP, player_one_up, player_two_up]:
                    if selection == 0: selection = len(options) - 1
                    else: selection -= 1

        screen.fill(BLACK)

        for i in range(len(options)):
            if i == selection:
                blinker = not blinker
                if blinker: continue
            text = font.render(options[i]['Text'], False, COLOUR).convert_alpha()
            screen.blit(text, (SCREEN_SIZE[0]//2 - text.get_width()//2,
                               SCREEN_SIZE[1]//4 + font.get_linesize() * 2 * i))

        pygame.display.update()

def load_settings() -> None:
    settings_path = Path(SETTINGS_PATH)
    if settings_path.is_file():
        with open(SETTINGS_PATH, 'r') as settings_file:
            settings = json.load(settings_file)
            for item in settings:
                globals()[item] = settings[item]
    else:
        default_settings = {'COLOUR':COLOUR,
                'player_one_up':player_one_up,
                'player_one_down':player_one_down,
                'player_two_up':player_two_up,
                'player_two_down':player_two_down,
                'points_per_game':points_per_game}
        with open(SETTINGS_PATH, 'w') as settings_file:
            json.dump(default_settings, settings_file)

if __name__ == '__main__':
    load_settings()
    #display_intro()
    main_menu()

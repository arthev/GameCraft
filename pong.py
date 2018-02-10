import pygame
import colour_constants
import random

SCREEN_SIZE = (640, 480)
BALL_DIAMETER = 32
MAX_FPS = 60
PADDLE_SIZE = (16, 64)
PADDLE_VEL = 10
HORIZONTAL_BAR = (SCREEN_SIZE[0], PADDLE_SIZE[0])
RECENT_HIT_RESET = 20

BLACK     = colour_constants.DISPLAYBLACK 
COLOUR    = colour_constants.APPLE2
PUREBLACK = colour_constants.PUREBLACK #Easy access for colorkeying

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)

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
            #Handle AI
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
        print("The ball collided with the", paddle.side, "paddle!")
        self.vel.x *= -1.05
        #TODO: Implement fun system calculating new velocities depending on where on the paddle the ball hit.

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
        self.font = pygame.font.SysFont("Mono", 32)

    def draw(self, left, right): #Idea for improved performance: Check whether there's a change to a score and then only rendering if so.
        left_text  = self.font.render(str(left),  True, COLOUR).convert_alpha()
        right_text = self.font.render(str(right), True, COLOUR).convert_alpha()
        y_offset = HORIZONTAL_BAR[1] * 1.5
        screen.blit(left_text,  (SCREEN_SIZE[0]//2 - 32 - left_text.get_width(),  y_offset))
        screen.blit(right_text, (SCREEN_SIZE[0]//2 + 32, y_offset))


def play() -> None:
    clock = pygame.time.Clock()

    background = Play_Background()
    scoredrawer = Scoredrawer()
    ball = Ball()
    paddle1 = Paddle(side="left", player=True, up_button=pygame.K_q, down_button=pygame.K_a)
    paddle2 = Paddle(side="right", player=True, up_button=pygame.K_o, down_button=pygame.K_l)
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
            else:
                paddles[1].score += 1
            print(scorer, "has scored! Current score: Left -", paddles[0].score, " :: Right -", paddles[1].score)
            ball.reset()

        scoredrawer.draw(paddles[0].score, paddles[1].score)
        ball.draw()
        for paddle in paddles: paddle.draw()
        pygame.display.update()

if __name__ == '__main__':
    play()

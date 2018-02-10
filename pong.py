import pygame
import colour_constants

SCREEN_SIZE = (640, 480)
BALL_DIAMETER = 32
MAX_FPS = 60
PADDLE_SIZE = (16, 64)
PADDLE_VEL = 10
HORIZONTAL_BAR = (SCREEN_SIZE[0], PADDLE_SIZE[0])

BLACK     = colour_constants.DISPLAYBLACK 
COLOUR    = colour_constants.APPLE2
PUREBLACK = colour_constants.PUREBLACK #Easy access for colorkeying

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)

def draw_play_background() -> None:
    screen.fill(BLACK) 

class Play_Background:
    def __init__(self) ->None:
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




class Ball:
    def __init__(self) -> None:
        self.pos = vector2(SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2)
        self.vel = vector2(SCREEN_SIZE[0]/2,  SCREEN_SIZE[1]/2)
        self.surface = pygame.Surface( (BALL_DIAMETER, BALL_DIAMETER) )
        self.surface.set_colorkey(PUREBLACK)
        pygame.draw.circle( self.surface, COLOUR, (BALL_DIAMETER//2, BALL_DIAMETER//2), BALL_DIAMETER//2)
        self.surface = self.surface.convert_alpha()

    def move(self, time_passed) -> None:
        self.pos.x += self.vel.x * time_passed
        self.pos.y += self.vel.y * time_passed
        if self.pos.x < 0 or self.pos.x + BALL_DIAMETER > SCREEN_SIZE[0]:
            self.vel.x *= -1
            if self.pos.x < 0:
                self.pos.x = 0
            else:
                self.pos.x = SCREEN_SIZE[0] - BALL_DIAMETER
        if self.pos.y < 0 or self.pos.y + BALL_DIAMETER > SCREEN_SIZE[1]:
            self.vel.y *= -1
            if self.pos.y < 0:
                self.pos.y = 0
            else:
                self.pos.y = SCREEN_SIZE[1] - BALL_DIAMETER

    def draw(self) -> None:
        screen.blit(self.surface, (self.pos.x, self.pos.y))

class Paddle:
    def __init__(self, side, player, up_button=None, down_button=None) -> None:
        if side == "left":
            self.pos = vector2(SCREEN_SIZE[0]//40, SCREEN_SIZE[1]//2 - PADDLE_SIZE[1]//2)
        elif side == "right":
            self.pos = vector2(SCREEN_SIZE[0] - PADDLE_SIZE[0] - SCREEN_SIZE[0]//40, SCREEN_SIZE[1]//2 - PADDLE_SIZE[1]//2)
        else:
            raise ValueError("Illegal 'side' argument sent to Paddle.__init__:", side)
        if player and (up_button == None or up_button == None):
            raise ValueError("Illegal combination of player and buttons sent to Paddle.__init__. None buttons make no sense for player == True")
        self.player = player
        self.up_button = up_button
        self.down_button = down_button
        self.vel = vector2(0, 0) #No initial movement.
        self.surface = pygame.Surface( (PADDLE_SIZE[0], PADDLE_SIZE[1]) )
        self.surface.fill(COLOUR)
        self.surface = self.surface.convert()

    def move(self, time_passed) -> None:
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
        self.pos.y += self.vel.y * time_passed


    def draw(self) -> None:
        screen.blit(self.surface, (self.pos.x, self.pos.y))





        





def play() -> None:
    clock = pygame.time.Clock()

    background = Play_Background()
    ball = Ball()
    paddle1 = Paddle(side="left", player=True, up_button=pygame.K_q, down_button=pygame.K_a)
    paddle2 = Paddle(side="right", player=True, up_button=pygame.K_o, down_button=pygame.K_l)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.constants.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()

        time_passed = clock.tick(MAX_FPS) / 1000.0 #time_passed is in seconds

        background.draw()

        ball.move(time_passed)
        paddle1.move(time_passed)
        paddle2.move(time_passed)


        ball.draw()
        paddle1.draw()
        paddle2.draw()
        pygame.display.update()














if __name__ == '__main__':
    play()

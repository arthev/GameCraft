import pygame
import colour_constants

SCREEN_SIZE = (640, 480)
BALL_DIAMETER = 32
MAX_FPS = 60

BLACK     = colour_constants.DISPLAYBLACK 
COLOUR    = colour_constants.APPLE2
PUREBLACK = colour_constants.PUREBLACK #Easy access for colorkeying

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)

def draw_play_background() -> None:
    screen.fill(BLACK) 

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







def play() -> None:
    clock = pygame.time.Clock()

    ball = Ball()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.constants.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()

        time_passed = clock.tick(MAX_FPS) / 1000.0 #time_passed is in seconds

        draw_play_background()
        ball.move(time_passed)
        ball.draw()

        pygame.display.update()














if __name__ == '__main__':
    play()

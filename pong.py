import pygame

SCREEN_SIZE = (640, 480)


pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)












def play():
    clock = pygame.time.Clock()

    ball = Ball()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.constants.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()

        time_passed = clock.tick(50) / 1000.0 #time_passed is in seconds

        draw_background()
        ball.move(time_passed)
        ball.draw()

        pygame.display.update()














if __name__ == '__main__':
    play()

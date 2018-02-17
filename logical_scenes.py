from Vector2 import *

class Game_Scene(Scene):
    class Paddle:
        def __init__(self):
            self.w = BW
            self.h = BH
            self.vel = Vector2(0, 0)
            self.starting_pos()
            self.create_surface()

        def create_surface(self):
            new = pygame.Surface( (self.w, self.h) )
            new.fill(COLOUR)
            self.sur = new.convert()

        def starting_pos(self):
            self.x = HW - self.w//2
            self.y = SCREEN_SIZE[1] - self.h
            self.vel.x = 0

        def move(self, time_passed):
            #Accelerate
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[right_button]: 
                self.vel.x += PADDLE_VEL*time_passed
            elif pressed_keys[left_button]: 
                self.vel.x -= PADDLE_VEL*time_passed
            else:
                if abs(self.vel.x) < 1: self.vel.x = 0
                else:
                    if self.vel.x < 0: sign = -1
                    else: sign = 1
                    friction = time_passed*fps*PADDLE_FRICTION*sign
                    self.vel.x -= friction
            #Move
            self.x += self.vel.x*time_passed
            if self.x < 0 or self.x > SCREEN_SIZE[0] - self.w:
                self.vel.x *= -0.80
                if self.x < 0:
                    self.x = 0
                else:
                    self.x = SCREEN_SIZE[0] - self.w

        def draw(self):
            screen.blit(self.sur, (self.x, self.y))
#"--------------------------------------------------------------------"
    class Ball:
        def __init__(self):
            self.r = BH//4
            self.starting_pos()
            self.create_surface()

        def create_surface(self):
            new = pygame.Surface( (2*self.r, 2*self.r) )
            new.set_colorkey(PUREBLACK)
            pygame.draw.circle(new, COLOUR, (self.r, self.r), self.r)
            self.sur = new.convert_alpha()

        def starting_pos(self):
            self.x = HW - self.r
            self.y = SCREEN_SIZE[1] - BH - self.r
            self.vel = Vector2(random.random()*300, random.random()*300)
            self.recent_hit = 0

        def move(self, time_passed, paddle, bmap): 
            #Returns (x, y) for collided-with brick (or None)
            def check_screen_boundaries():
                if self.x < 0 + self.r or self.x > SCREEN_SIZE[0] - self.r:
                    self.vel.x *= -1
                    if self.x < 0 + self.r:
                        self.x = self.r
                    else:
                        self.x = SCREEN_SIZE[0] - self.r
                if self.y < DVOFFSET + self.r or self.y > SCREEN_SIZE[1] - self.r:
                    self.vel.y *= -1
                    if self.y < DVOFFSET + self.r:
                        self.y = DVOFFSET + self.r
                    else:
                        self.y = SCREEN_SIZE[1] - self.r

            def paddle_collision_handler():
                def simple_check():
                    if self.y + self.r < SCREEN_SIZE[1] - paddle.h:
                        return False
                    if self.x + self.r < paddle.x or self.x - self.r > paddle.x + paddle.w:
                        return False
                    return True
                def paddle_collision():
                    steps = paddle.w + self.r
                    extreme = 1.12
                    hit = self.x - (paddle.x + paddle.w//2)
                    w = extreme/steps*hit
                    newVec = 0 #This is unit vector soon...
                    newVec = Vector2(-math.sin(w), math.cos(w))
                    mag = self.vel.get_magnitude() * GAME_INTENSIFYING_CONSTANT * -1
                    self.vel.normalize()
                    newVec = newVec + self.vel
                    newVec.normalize()
                    newVec = newVec * mag
                    self.vel = newVec

                if simple_check():
                    if self.recent_hit <= 0:
                        paddle_collision()
                        self.recent_hit = RECENT_HIT_RESET

            def brick_collision_handler():
                gx = int(self.x // BW)
                gy = int(self.y // BH - VOFFSET)
                if bmap[gx][gy] != 0:
                    return (gx, gy)
                horiz = 0
                rx = self.x / BW - gx
                if rx < self.r / BW:
                    horiz = -1
                elif abs(rx-1) < self.r / BW:
                    horiz = 1
                vertic = 0
                ry = self.y / BH - gy
                if ry < self.r / BH:
                    vertic = -1
                elif abs(ry-1) < self.r / BH:
                    vertic = 1
                if horiz == 0 and vertic == 0:
                    return None
                fx = gx + horiz
                fy = gy + vertic
                if bmap[fx][fy] == 0:
                    return None
                if horiz != 0:
                    self.vel.x *= -1
                if vertic != 0:
                    self.vel.y *= -1
                return (gx + horiz, gy + vertic)








            self.recent_hit -= 1
            self.x += self.vel.x * time_passed
            self.y += self.vel.y * time_passed
            check_screen_boundaries()
            paddle_collision_handler()
            return brick_collision_handler()

        def draw(self):
            screen.blit(self.sur, (self.x - self.r, self.y - self.r))






#"-------------------------------------------------------------------"
    def goto_pause(self):
        add_scene(Pause())

    def load_level(self):
        fn = os.path.join(MAP_DIR, str(self.level)+".abrm")
        if os.path.isfile(fn):
            with open(fn, 'r') as f:
                build_map = {}
                jmap = json.load(f)
                for i in jmap:
                    build_map[int(i)] = jmap[i]
                return build_map
        else:
            print(fn, "could not be found! Shutting down...")
            exit()

    #Move from one stage to the next by creating a new game scene with
    #the appropriate init call, including sending old lives and paddles
    #forwards, hehe.
    def __init__(self, level=1, paddle=None, lives=None, ball=None):
        self.level = level
        self.bmap = self.load_level()
        self.score = 0
        self.clock = pygame.time.Clock()
        if not paddle: self.paddle = self.Paddle()
        else: self.paddle = paddle
        if not lives: self.lives = lives_setting
        else: self.lives = lives
        if not ball: self.ball = self.Ball()
        else: self.ball = ball
        self.ball.starting_pos()
        self.paddle.starting_pos()

    def update(self):
        time_passed =  self.clock.tick(fps) / 1000.0 #in seconds

        for event in pygame.event.get():
            if event.type == pygame.constants.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                elif event.key == pause_button:
                    self.goto_pause()

        self.paddle.move(time_passed)
        collided_brick = self.ball.move(time_passed, self.paddle, self.bmap)
        if collided_brick:
            #TODO: implement better handling here
            bx, by = collided_brick
            self.bmap[bx][by] = 0
            print("Collided at", collided_brick[0], collided_brick[1])



    def board_won(self):
        #TODO: Check if all bricks are 0
        pass

    def game_over(self):
        N = 6
        if N % 2 == 0: N += 1
        for i in range(N):
            self.clock.tick(N//2)
            if i % 2 == 0: self.draw()
            else: screen.fill(BLACK)
            pygame.display.update()
        self.clock.tick(N//2)
        add_scene(Game_Over(self.score))

    def draw(self):
        screen.fill(BLACK)

        pygame.draw.line(screen, COLOUR, 
                (0, DVOFFSET - 2), (SCREEN_SIZE[0], DVOFFSET - 2))
        for i in self.bmap:
            for j, e in enumerate(self.bmap[i]):
                if e == 0: continue
                screen.blit(block_surfaces[e],
                        (i*BW, (j+VOFFSET)*BH))
                self.paddle.draw()
        self.ball.draw()








class High_Score_Entry(Scene):
    def save_scores(self):
        with open(str(HIGHSCORE_PATH), 'w') as score_file:
            json.dump(high_scores, score_file)

    def no_score(self):
        scene_stack.pop()

    def yes_score(self):
        high_scores[self.hit] = {"name":self.name, "score":self.score}
        self.save_scores()
        scene_stack.pop()
        scene_stack.append(High_Score_View())

    def __init__(self, score):
        if score <= high_scores["5"]["score"]:
            self.no_score()
            return
        self.score = score
        self.hit = "5"
        for i in range(5, 0, -1):
            if score > high_scores[str(i)]["score"]:
                self.hit = str(i)
        for i in range(5, int(self.hit), -1):
            high_scores[str(i)] = high_scores[str(i-1)]
        self.name = ""

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.constants.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    self.name += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    if self.name == "": pass
                    else: self.name = self.name[:-1]
                elif event.key == pygame.K_RETURN:
                    self.yes_score()

    def draw(self):
        screen.fill(BLACK)
        text = global_font.render("New highscore! Enter your name...", False, COLOUR).convert_alpha()
        screen.blit(text, (HALF_WIDTH - text.get_width()//2,
            HALF_HEIGHT - global_font.get_linesize()//2))
        nametext = global_font.render(self.name, False, COLOUR).convert_alpha()
        screen.blit(nametext, (HALF_WIDTH - nametext.get_width()//2,
            HALF_HEIGHT + global_font.get_linesize()//2))




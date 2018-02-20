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
            self.ghost_ball = False

        def create_surface(self):
            new = pygame.Surface( (2*self.r, 2*self.r) )
            new.set_colorkey(PUREBLACK)
            pygame.draw.circle(new, COLOUR, (self.r, self.r), self.r)
            self.sur = new.convert_alpha()

        def starting_pos(self):
            self.x = HW - self.r
            self.y = SCREEN_SIZE[1] - BH - self.r
            self.vel = Vector2(0, BALL_START_VEL)
            self.shot = False

        def shoot(self):
            self.shot = True

        def ghost_ballify(self):
            self.ghost_ball = True

        def move(self, time_passed, paddle, bmap): 
            #Returns (x, y) for collided-with brick (or None)
            def check_screen_boundaries():
                if self.x < 0 + self.r or self.x > SCREEN_SIZE[0] - self.r:
                    self.vel.x *= -1
                    if self.x < 0 + self.r:
                        self.x = self.r
                    else:
                        self.x = SCREEN_SIZE[0] - self.r
                if self.y < DVOFFSET + self.r:
                    self.vel.y *= -1
                    self.y = DVOFFSET + self.r

            def paddle_collision_handler():
                def simple_check():
#                    if self.y + self.r < SCREEN_SIZE[1] - paddle.h:
 #                       return False
  #                  if self.x + self.r < paddle.x or self.x - self.r > paddle.x + paddle.w:
   #                     return False
    #                return True
                    x_lower = self.x < paddle.x + paddle.w
                    x_higher = self.x + self.r > paddle.x
                    y_lower = self.y < paddle.y + paddle.h
                    y_higher = self.y + self.r > paddle.y
                    return x_lower and x_higher and y_lower and y_higher
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

                    #Trying to set it above the paddle as well, and then maybe get rid of RECENT_HIT_RESET.
                    self.y = paddle.y - self.r

                if simple_check():
#                    if self.recent_hit <= 0:
                    paddle_collision()
                    #    self.recent_hit = RECENT_HIT_RESET

            def brick_collision_handler():
                def x2x(x): return min(int(x//BW), max(bmap))
                def y2y(y): return min(int(y//BH) - VOFFSET, len(bmap[0]) - 1)
                gx = x2x(self.x)
                gy = y2y(self.y)
                to_return = None
                reverse_x = False
                reverse_y = False
                #Handle adjacents
                if bmap[gx][gy] != 0:
                    if random.random() < 0.1:
                        reverse_x = True
                    else:
                        reverse_y = True
                    to_return = (gx, gy)
                if self.vel.x > 0 and not to_return:
                    dx = x2x(self.x + self.r)
                    if dx != gx and bmap[dx][gy] != 0:
                        reverse_x = True
                        to_return = (dx, gy)
                if self.vel.x < 0 and not to_return: 
                    dx = x2x(self.x - self.r)
                    if dx != gx and bmap[dx][gy] != 0:
                        reverse_x = True
                        to_return = (dx, gy)
                if self.vel.y > 0 and not to_return:
                    dy = y2y(self.y + self.r)
                    if dy != gy and bmap[gx][dy] != 0:
                        reverse_y = True
                        to_return = (gx, dy)
                if self.vel.y < 0 and not to_return:
                    dy = y2y(self.y - self.r)
                    if dy != gy and bmap[gx][dy] != 0:
                        reverse_y = True
                        to_return = (gx, dy)
                #No adjacents? Let's check for diagonals.
                if to_return == None:
                    d = math.sqrt(2*self.r**2)/2
                    if self.vel.x > 0: xdir = 1
                    else: xdir = -1
                    if self.vel.y > 0: ydir = 1
                    else: ydir = -1

                    if x2x(self.x + d*xdir) == gx + xdir and y2y(self.y + d*ydir) == gy + ydir:
                        if bmap[gx+xdir][gy+ydir] != 0:
                           reverse_x = True
                           reverse_y = True
                           to_return = (gx + xdir, gy + ydir)

                if not self.ghost_ball:
                    if reverse_x:
                        self.vel.x *= -1
                    if reverse_y:
                        self.vel.y *= -1
                return to_return

            if not self.shot:
                self.x = paddle.x + paddle.w//2
                return None
            self.x += self.vel.x * time_passed
            self.y += self.vel.y * time_passed
            check_screen_boundaries()
            paddle_collision_handler()
            return brick_collision_handler()

        def death(self):
            return self.y - self.r > SCREEN_SIZE[1]

        def draw(self):
            screen.blit(self.sur, (self.x - self.r, self.y - self.r))
#"-------------------------------------------------------------------"
    class Powerup:
        def enlarge_paddle(self): 
            self.paddle.w = min(self.paddle.w + BW//8, SCREEN_SIZE[0])
            if self.paddle.w + BW//8 > SCREEN_SIZE[0]:
                self.paddle.w = SCREEN_SIZE[0]
                self.paddle.x = 0
            else:
                self.paddle.w += BW//8
                self.paddle.x = max(0, min(self.paddle.x - BW//16, SCREEN_SIZE[0] - self.paddle.w))
            self.paddle.create_surface()
        def shrink_paddle(self):
            if self.paddle.w <= BW//32:
                pass
            elif self.paddle.w - BW//8 < BW//32:
                diff = abs(self.paddle.w - BW//8 - BW//32)
                self.paddle.w = BW//32
                self.paddle.x += diff//2
                if self.paddle.x + self.paddle.w > SCREEN_SIZE[0]:
                    self.paddle.x = SCREEN_SIZE[0] - self.paddle.w
            else:
                self.paddle.w -= BW//8
                self.paddle.x += BW//16
            self.paddle.create_surface()
        def enlarge_ball(self):
            if self.ball.r < BW//2:
                self.ball.r += 2
                self.ball.create_surface()
        def shrink_ball(self):
            if self.ball.r > BW//64:
                self.ball.r -= 2
                if self.ball.r < BW//64:
                    self.ball.r = BW//64
                self.ball.create_surface()
        def extra_life(self):
            self.game.lives += 1
            self.game.set_life_surface()
        def death_up(self):
            self.game.die()
        def ghost_ball(self):
            self.ball.ghost_ballify()


        surfaci = {}
        ps = BW//2
        base_sur = pygame.Surface( (ps, ps) )
        base_sur.fill(BLACK)
        pygame.draw.rect(base_sur, COLOUR, (0, 0, ps, ps), ps//16)

        e_sur = base_sur.copy()
        pygame.draw.polygon(e_sur, COLOUR,
                ( (ps//16, ps//2), (ps//2 - ps//8, ps//4),
                    (ps//2 - ps//8, 3*ps//4) ) )
        pygame.draw.polygon(e_sur, COLOUR,
                ( (ps - ps//16, ps//2), (ps//2 + ps//8, ps//4),
                    (ps//2 + ps//8, 3*ps//4) ) )
        e_sur = e_sur.convert()
        surfaci["enlarge_paddle"] = e_sur

        s_sur = base_sur.copy()
        pygame.draw.polygon(s_sur, COLOUR,
                ( (ps//2 - ps//8, ps//2), (ps//8, ps//4),
                    (ps//8, 3*ps//4) ) )
        pygame.draw.polygon(s_sur, COLOUR,
                ( (ps//2 + ps//8, ps//2), (ps - ps//8, ps//4),
                    (ps - ps//8, 3*ps//4) ) )
        s_sur = s_sur.convert()
        surfaci["shrink_paddle"] = s_sur

        be_sur = base_sur.copy()
        pygame.draw.circle(be_sur, COLOUR,
                (ps//2, ps//2), 4)
        pygame.draw.lines(be_sur, COLOUR, False,
                [(ps//2, ps//8), (ps - ps//8, ps//8),
                    (ps - ps//8, ps//2), (ps - ps//8, ps//8),
                    (ps//2, ps//2)], 1)
        pygame.draw.lines(be_sur, COLOUR, False,
                [(ps//2, ps - ps//8), (ps//8, ps - ps//8),
                    (ps//8, ps//2), (ps//8, 7*ps//8),
                    (ps//2, ps//2)], 1)
        be_sur = be_sur.convert()
        surfaci["enlarge_ball"] = be_sur

        bs_sur = base_sur.copy()
        pygame.draw.circle(bs_sur, COLOUR,
                (ps//2, ps//2), 4)
        pygame.draw.lines(bs_sur, COLOUR, False,
                [(ps//8, ps//8), (ps//3, ps//3),
                    (ps//3, ps//8), (ps//3, ps//3),
                    (ps//8, ps//3)], 1)
        pygame.draw.lines(bs_sur, COLOUR, False,
                [(7*ps//8, 7*ps//8), (2*ps//3, 2*ps//3),
                    (2*ps//3,7*ps//8), (2*ps//3, 2*ps//3),
                    (7*ps//8, 2*ps//3)], 1)
        bs_sur = bs_sur.convert()
        surfaci["shrink_ball"] = bs_sur

        el_sur = base_sur.copy()
        pygame.draw.polygon(el_sur, COLOUR,
                [(ps//2, 7*ps//8), (ps//8, ps//2), (7*ps//8, ps//2)])
        pygame.draw.circle(el_sur, COLOUR,
                (ps//3, ps//2), ps//5)
        pygame.draw.circle(el_sur, COLOUR,
                (2*ps//3 + ps//16, ps//2), ps//5)
        el_sur = el_sur.convert()
        surfaci["extra_life"] = el_sur

        d_sur = base_sur.copy()
        pygame.draw.circle(d_sur, COLOUR,
                (ps//4, ps//4), ps//8)
        pygame.draw.circle(d_sur, COLOUR,
                (3*ps//4, ps//4), ps//8)
        pygame.draw.circle(d_sur, COLOUR,
                (ps//4, 3*ps//4), ps//8)
        pygame.draw.circle(d_sur, COLOUR,
                (3*ps//4, 3*ps//4), ps//8)
        pygame.draw.line(d_sur, COLOUR,
                (ps//4, ps//4), (3*ps//4, 3*ps//4), ps//8)
        pygame.draw.line(d_sur, COLOUR,
                (ps//4, 3*ps//4), (3*ps//4, ps//4), ps//8)
        d_sur = d_sur.convert()
        surfaci["death_up"] = d_sur

        g_sur = base_sur.copy()
        pygame.draw.circle(g_sur, COLOUR,
                (ps//2, ps//2), ps//3)
        pygame.draw.rect(g_sur, BLACK,
                (ps//16, ps//16, ps//2, 15*ps//16))
        pygame.draw.line(g_sur, COLOUR, 
                (ps//2, 0), (ps//2, ps), ps//16)
        g_sur = g_sur.convert()
        surfaci["ghost_ball"] = g_sur


        effects = {}
        effects["enlarge_paddle"] = enlarge_paddle
        effects["shrink_paddle"] = shrink_paddle
        effects["enlarge_ball"] = enlarge_ball
        effects["shrink_ball"] = shrink_ball
        effects["extra_life"] = extra_life
        effects["death_up"] = death_up
        effects["ghost_ball"] = ghost_ball


        tableaux = [(5, "extra_life"), (15, "death_up"),
                (40, "shrink_ball"), (65, "shrink_paddle"),
                (80, "enlarge_ball"), (95, "enlarge_paddle"),
                (100, "ghost_ball")]
        def __init__(self, x, y, paddle, ball, game):
            self.x = x*BW + BW//2 - self.ps//2
            self.y = y
            self.paddle = paddle
            self.ball = ball
            self.game = game
            indicator = random.randint(1, 100)
            for e in self.tableaux:
                if indicator <= e[0]:
                    self.type = e[1]
                    break

        def move(self):
            self.y += 4
            if self.x < self.paddle.x + self.paddle.w and self.x + self.ps > self.paddle.x:
                if self.y < self.paddle.y + self.paddle.h and self.y + self.ps > self.paddle.y:
                    #collision!
                    self.y += 1000 #This will make the game update destruct the powerup in the next frame
                    self.effects[self.type](self)
                    self.game.add_score(30)

        def draw(self):
            screen.blit(self.surfaci[self.type], (self.x, self.y))
#"-------------------------------------------------------------------"
    def goto_pause(self):
        add_scene(Pause())
        self.flush_clock = True

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
            print("file not found despite pre-testing:", fn)
            print("Shutting down...")

    def set_life_surface(self):
        s = DVOFFSET
        n_sur = pygame.Surface( (s, s) )
        n_sur.fill(BLACK)
        pygame.draw.polygon(n_sur, COLOUR,
                ( (s//2, s - s//12), (s//16, s//3), (s - s//16, s//3)))
        pygame.draw.circle(n_sur, COLOUR,
                ( (s//2 - s//12)//2 + s//12,   s//3),
                  (s//2 - s//12)//2)
        pygame.draw.circle(n_sur, COLOUR,
                ( (s//2 + (s - s//6)//4), s//3),
                 (s//2 - s//12)//2)

        x_font = pygame.font.SysFont("Mono", gfont.get_height()//4, bold=True)
        x_sur = x_font.render("x", False, COLOUR)
        m_sur = gfont.render(str(self.lives), False, COLOUR)
        t_sur = pygame.Surface( 
                (n_sur.get_width() + x_sur.get_width() + m_sur.get_width(), s))
        t_sur.fill(BLACK)
        t_sur.blit(m_sur, (0, s//2 - m_sur.get_height()//2))
        t_sur.blit(x_sur, (m_sur.get_width(), s//2 - x_sur.get_height()//2))
        t_sur.blit(n_sur, (t_sur.get_width() - n_sur.get_width(), 0))
        self.h_sur = t_sur.convert()


    #Move from one stage to the next by creating a new game scene with
    #the appropriate init call, including sending old lives and paddles
    #forwards, hehe.
    def __init__(self, level=1, paddle=None, lives=None, ball=None, score=0):

        global unlocked_level
        self.score = score
        self.level = level
        self.bmap = self.load_level()
        self.clock = pygame.time.Clock()
        if not paddle: self.paddle = self.Paddle()
        else: self.paddle = paddle
        if not lives: self.lives = lives_setting
        else: self.lives = lives
        if not ball: self.ball = self.Ball()
        else: self.ball = ball
        self.ball.starting_pos()
        self.paddle.starting_pos()
        self.powerups = []
        if self.level > unlocked_level:
            unlocked_level = self.level
            save_settings()
        
        self.l_sur = gfont.render("Level - " + str(self.level), False, COLOUR).convert_alpha()
        self.set_life_surface()
        self.flush_clock = False


    def update(self):
        self.just_died = False
        if self.flush_clock:
            self.flush_clock = False
            self.clock.tick()
        time_passed =  self.clock.tick(fps) / 1000.0 #in seconds
        suicide = False

        for event in pygame.event.get():
            if event.type == pygame.constants.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                elif event.key == pause_button:
                    self.goto_pause()
                elif event.key == shoot_button:
                    self.ball.shoot()
                elif event.key == suicide_button:
                    suicide = True
                elif event.key == pygame.K_w:
                    self.ball.ghost_ballify()

        self.paddle.move(time_passed)
        for p in self.powerups:
            p.move()
        for i in range(len(self.powerups) - 1, -1, -1):
            if self.powerups[i].y > SCREEN_SIZE[1]:
                self.powerups.pop(i)
        collided_brick = self.ball.move(time_passed, self.paddle, self.bmap)
        if collided_brick:
            self.brick_hit_handler(collided_brick)
        death = self.ball.death()
        if death or suicide:
            self.die()
        self.board_won()

    def die(self):
        self.just_died = True
        self.lives -= 1
        if self.lives < 0:
            self.game_over()
        else:
            self.ball = self.Ball()
            self.paddle = self.Paddle()
            self.set_life_surface()
            self.powerups = []
            add_scene(Death_Animation())
            self.flush_clock = True

    def brick_hit_handler(self, brick):
        bx, by = brick
        v = self.bmap[bx][by]
        destroyed = False
        extra_score = 0
        if v == 1:
            if self.ball.ghost_ball:
                destroyed = True
                extra_score += 25
        elif v == 3:
            if self.ball.ghost_ball:
                destroyed = True
                extra_score += 15
            else:
                extra_score += 5
                self.bmap[bx][by] = 2
        else:
            destroyed = True
            extra_score += 10
        if destroyed:
            self.bmap[bx][by] = 0
            self.maybe_spawn_powerup(bx, by)
        self.add_score(extra_score)

    def add_score(self, bonus):
        self.score += round(bonus * (BALL_START_VEL/100) * 64/PADDLE_START_WIDTH * 4/lives_setting)
            
    def maybe_spawn_powerup(self, bx, by):
        if random.random() < POWERUP_CHANCE:
            self.powerups.append(self.Powerup(bx, by, self.paddle, self.ball, self))

    def board_won(self):
        for x in self.bmap:
            for y, e in enumerate(self.bmap[x]):
                if not (e == 0 or e == 1):
                    return
        #If execution goes here, the board's clear.
        fn = os.path.join(MAP_DIR, str(self.level + 1) + ".abrm")
        if os.path.isfile(fn):
            change_scene(Game_Scene(level = self.level + 1,
                    paddle=self.paddle, lives = self.lives,
                    ball=self.ball, score=self.score))
        else:
            change_scene(Game_Won(self.score))

    def game_over(self):
        self.just_died = False #To permit drawing lol
        N = 6
        if N % 2 == 0: N += 1
        for i in range(N):
            self.clock.tick(N//2)
            if i % 2 == 0: self.draw()
            else: screen.fill(BLACK)
            pygame.display.update()
        self.clock.tick(N//2)
        change_scene(Game_Over(self.score))

    def draw(self):
        if self.just_died: return
        screen.fill(BLACK)

        screen.blit(self.l_sur,
                (HW - self.l_sur.get_width()//4, 
                    DVOFFSET//2 - self.l_sur.get_height()//2))
        screen.blit(gfont.render("Score: " + str(self.score), False, COLOUR),
                (0, DVOFFSET//2 - gfont.get_height()//2))
        screen.blit(self.h_sur,
                (SCREEN_SIZE[0] - self.h_sur.get_width(), 0))



        pygame.draw.line(screen, COLOUR, 
                (0, DVOFFSET - 2), (SCREEN_SIZE[0], DVOFFSET - 2))
        for i in self.bmap:
            for j, e in enumerate(self.bmap[i]):
                if e == 0: continue
                screen.blit(block_surfaces[e],
                        (i*BW, (j+VOFFSET)*BH))
        for p in self.powerups:
            p.draw()
        self.paddle.draw()
        self.ball.draw()








class High_Score_Entry(Scene):
    def save_scores(self):
        with open(str(HIGHSCORE_PATH), 'w') as score_file:
            json.dump(high_scores, score_file)

    def no_score(self):
        pop_scene()

    def yes_score(self):
        high_scores[self.hit] = {"name":self.name, "score":self.score}
        self.save_scores()
        change_scene(High_Score_View())

    def __init__(self, score):
        if score <= high_scores["5"]["score"]:
            self.flag = True
            return
        else:
            self.flag = False
            self.score = score
            self.hit = "5"
            for i in range(5, 0, -1):
                if score > high_scores[str(i)]["score"]:
                    self.hit = str(i)
            for i in range(5, int(self.hit), -1):
                high_scores[str(i)] = high_scores[str(i-1)]
            self.name = ""

    def update(self):
        if self.flag:
            self.no_score()
            return
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
        if self.flag:
            return
        screen.fill(BLACK)
        text = gfont.render("New highscore! Enter your name...", False, COLOUR).convert_alpha()
        screen.blit(text, (HW - text.get_width()//2,
            HH - gfont.get_linesize()//2))
        nametext = gfont.render(self.name, False, COLOUR).convert_alpha()
        screen.blit(nametext, (HW - nametext.get_width()//2,
            HH + gfont.get_linesize()//2))

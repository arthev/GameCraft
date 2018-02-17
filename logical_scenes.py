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




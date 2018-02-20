class Overlay_Scene(Scene):
    def cont(self): 
        pop_scene()
        try: self.clock.tick(fps)
        except AttributeError: pass

    def __init__(self, clock = None):
        self.background = pygame.Surface.copy(screen)
        self.overlay = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
        pygame.draw.rect(self.overlay, (0, 0, 0, 205), (0, 0, SCREEN_SIZE[0], SCREEN_SIZE[1]))
        self.clock = clock

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

class High_Score_View(Overlay_Scene):
    def draw(self):
        screen.fill(BLACK)
        fifth = SCREEN_SIZE[1]//5
        for i in high_scores:
            name = high_scores[i]["name"]
            if name == None: name = ""
            score = high_scores[i]["score"]
            text = gfont.render("{:6} : {}".format(score, name), False, COLOUR).convert_alpha()
            screen.blit(text, (SCREEN_SIZE[0]//6, (int(i)-1)*fifth + fifth//3))

class Set_Key(Overlay_Scene):
    def cont(self, key):
        globals()[self.specified["var"]] = key
        pop_scene()

    def __init__(self, specified):
        self.specified = specified
        Overlay_Scene.__init__(self)

    def draw(self):
        Overlay_Scene.draw(self)
        text = gfont.render("Press desired key...", False, COLOUR).convert_alpha()
        screen.blit(text, (HW - text.get_width()//2,
                           HH- text.get_height()//2))

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
        text = gfont.render("Paused", False, COLOUR).convert_alpha()
        screen.blit(text, (HW - text.get_width()//2,
                           HH- text.get_height()//2))

class Game_Over(Overlay_Scene):
    def cont(self):
        change_scene(High_Score_Entry(self.score))

    def __init__(self, score):
        self.score = score
        Overlay_Scene.__init__(self)
    def draw(self):
        Overlay_Scene.draw(self)
        text = gfont.render("Game Over", False, COLOUR)
        screen.blit(text, (HW - text.get_width()//2,
                           HH-text.get_height()//2))

class Game_Won(Game_Over):
    def draw(self):
        Overlay_Scene.draw(self)
        text = gfont.render("You won!", False, COLOUR)
        screen.blit(text, (HW - text.get_width()//2,
                           HH - text.get_height()//2))
        text = gfont.render("CONGRATULATIONS!", False, COLOUR)
        screen.blit(text, (HW - text.get_width()//2,
                           HH + text.get_height()//2))

class Death_Animation(Overlay_Scene):
    def __init__(self, clock):
        self.i = 0
        Overlay_Scene.__init__(self, clock)
        new_overlay = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)

        pygame.draw.rect(new_overlay, (0, 0, 0, self.i), (0, 0, SCREEN_SIZE[0], SCREEN_SIZE[1]))
        self.overlay = new_overlay.convert_alpha()

    def update(self):
        if self.i < 255:
            self.i += 1

            pygame.draw.rect(self.overlay, (0, 0, 0, self.i), (0, 0, SCREEN_SIZE[0], SCREEN_SIZE[1]))
            pygame.time.wait(3)
        else:
            pygame.time.wait(700)
            self.cont()


class Splash_Screen(Overlay_Scene):
    def __init__(self):
        self.i = 0
        self.j = 0
        display_font = pygame.font.SysFont("Mono", SCREEN_SIZE[0]//12, bold=True)
        self.display_text = display_font.render("BreakoutyBreakout", False, COLOUR, BLACK).convert()
        display_font2 = pygame.font.SysFont("Mono", SCREEN_SIZE[0]//18, bold=True)
        self.display_text2 = display_font2.render("by: Arthur", False, COLOUR, BLACK).convert()
        self.display_text.set_alpha(0)
        self.display_text2.set_alpha(0)

    def update(self):
        Overlay_Scene.update(self)
        if self.i < 256:
            self.i += 1
            self.display_text.set_alpha(self.i)
            pygame.time.wait(10)
        elif self.j < 256:
            self.j += 1
            self.display_text2.set_alpha(self.i)
            pygame.time.wait(5)
        else:
            pygame.time.wait(250)
            self.cont()

    def draw(self):
        screen.fill(BLACK)
        screen.blit(self.display_text, 
                (HW - self.display_text.get_width()//2,
                 HH - self.display_text.get_height()))
        screen.blit(self.display_text2,
                (HW, HH))



class Board_Won(Overlay_Scene):
    def draw(self):
        Overlay_Scene.draw(self)
        text = gfont.render("Board Cleared! Well done!", False, COLOUR).convert_alpha()
        screen.blit(text, (HW - text.get_width()//2,
                           HH-text.get_height()//2 - gfont.get_linesize()//2))
        infotext = gfont.render("Press Return or Pause to continue.", False, COLOUR).convert_alpha()
        infotext = pygame.transform.scale(infotext, (round(infotext.get_width()*MENU_DWINDLE),
                                                     round(infotext.get_height()*MENU_DWINDLE)))
        screen.blit(infotext, (HW - infotext.get_width()//2,
                               HH-infotext.get_height()//2 + gfont.get_linesize()//2))

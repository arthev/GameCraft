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

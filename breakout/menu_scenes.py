class Menu_Scene(Scene):
    #{..., "surface": None, ...} for standard option display.
    def __init__(self, options, keybindings = None):
        if keybindings == None:
            self.keybindings = [{up_button: self.select_up},
                                {down_button: self.select_down},
                                {right_button: self.select_right},
                                {left_button: self.select_left},
                                {pygame.K_RETURN: self.call_selected},
                                {pygame.K_ESCAPE: exit}]
        else: self.keybindings = keybindings
        self.selection = 0
        self.options = options

    def get_select_up(self, from_index=None) -> int:
        if from_index == None: i = self.selection
        else: i = from_index
        if i == 0: return len(self.options) - 1
        else: return i - 1
    def get_select_down(self, from_index=None) -> int:
        if from_index == None: i = self.selection
        else: i = from_index
        if i == len(self.options) - 1: return 0
        else: return i + 1
    def select_up(self):
        self.selection = self.get_select_up()
    def select_down(self):
        self.selection = self.get_select_down()

    def select_right(self):
        cur = self.options[self.selection]
        if "right" in cur: cur["right"]()
    def select_left(self):
        cur = self.options[self.selection]
        if "left" in cur: cur["left"]()
    def call_selected(self):
        cur = self.options[self.selection]
        if "var" in cur: cur["func"](cur)
        else: cur["func"]()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.constants.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                for binding in self.keybindings:
                    if event.key in binding:
                        binding[event.key]()

    def get_base_surface(self, opt):
        if not opt["surface"]: return gfont.render(opt["text"], False, COLOUR).convert_alpha()
        elif "var" in opt: return opt["surface"](opt)
        else: return opt["surface"]()

    def draw(self):
        screen.fill(BLACK)

        c_sur = self.get_base_surface(self.options[self.selection])
        screen.blit(c_sur, (HW - c_sur.get_width()//2, 
                            HH - c_sur.get_height()//2))
        
        a_sur = self.get_base_surface(self.options[self.get_select_up()])
        a_sur = pygame.transform.smoothscale(a_sur, (round(a_sur.get_width()*MENU_DWINDLE),
                                                    (round(a_sur.get_height()*MENU_DWINDLE))))
        screen.blit(a_sur, (HW - a_sur.get_width()//2,
                            HH - a_sur.get_height() * 2))

        b_sur = self.get_base_surface(self.options[self.get_select_down()])
        b_sur = pygame.transform.smoothscale(b_sur, (round(b_sur.get_width()*MENU_DWINDLE),
                                                    (round(b_sur.get_height()*MENU_DWINDLE))))
        screen.blit(b_sur, (HW - b_sur.get_width()//2,
                              HH + b_sur.get_height()))

        aa_sur = self.get_base_surface(self.options[self.get_select_up(self.get_select_up())])
        aa_sur = pygame.transform.smoothscale(aa_sur, (round(aa_sur.get_width()*MENU_DWINDLE*MENU_DWINDLE),
                                                      round(aa_sur.get_height()*MENU_DWINDLE*MENU_DWINDLE)))
        screen.blit(aa_sur, (HW - aa_sur.get_width()//2,
                             HH - a_sur.get_height() * 2 - aa_sur.get_height() * 2))

        bb_sur = self.get_base_surface(self.options[self.get_select_down(self.get_select_down())])
        bb_sur = pygame.transform.smoothscale(bb_sur, (round(bb_sur.get_width()*MENU_DWINDLE*MENU_DWINDLE),
                                                      round(bb_sur.get_height()*MENU_DWINDLE*MENU_DWINDLE)))
        screen.blit(bb_sur, (HW - bb_sur.get_width()//2,
                             HH + b_sur.get_height() * 2 + bb_sur.get_height()))

   

    def arrow_surface(self, msg):
        text = gfont.render(msg, False, COLOUR).convert_alpha()

        h = text.get_height()*0.75//1
        arrows = pygame.Surface((h, h))
        arrows.fill(BLACK)
        pygame.draw.polygon(arrows, COLOUR,
                ( (0, h//2), (h//2 - h//8, h//4), (h//2 - h//8, 3*h//4) ) )
        pygame.draw.polygon(arrows, COLOUR,
                ( (h, h//2), (h//2 + h//8, h//4), (h//2 + h//8, 3*h//4) ) )
        c_sur = pygame.Surface((text.get_width() + arrows.get_width() + h//4,
                                 text.get_height()))
        c_sur.fill(BLACK)
        c_sur.blit(arrows, (0, h//8))
        c_sur.blit(text, (arrows.get_width() + h//4, 0))
        c_sur.convert_alpha()
        return c_sur


class Settings_Menu(Menu_Scene):
    def exit_settings(self):
        save_settings()
        os.execl(sys.executable, sys.executable, *sys.argv)

    def set_key(self, specifier):
        add_scene(Set_Key(specifier))


    def colour_surface(self):
        return self.arrow_surface("Colour")
    def colour_right(self):
        global COLOUR
        if self.colour_selection == len(COLOURLIST) - 1:
            self.colour_selection = 0
        else: self.colour_selection += 1
        COLOUR = COLOURLIST[self.colour_selection]
    def colour_left(self):
        global COLOUR
        if self.colour_selection == 0:
            self.colour_selection = len(COLOURLIST) - 1
        else: self.colour_selection -= 1
        COLOUR = COLOURLIST[self.colour_selection]

    def key_surface(self, specifier):
        key_name = pygame.key.name(globals()[specifier["var"]])
        return gfont.render(specifier["text"] + key_name, False, COLOUR).convert_alpha()

    def ball_speed_surface(self):
        return self.arrow_surface("Ball Speed: " + str(BALL_START_VEL//50))
    def ball_speed_right(self):
        global BALL_START_VEL
        BALL_START_VEL += 50
    def ball_speed_left(self):
        global BALL_START_VEL
        if BALL_START_VEL > 50:
            BALL_START_VEL -= 50
        

    def __init__(self):
        self.colour_selection = 0
        for i, colour in enumerate(COLOURLIST):
            if colour == COLOUR:
                self.colour_selection = i
        options = [{"text":"Colour", "func": ef, "surface":self.colour_surface,
                       "right":self.colour_right, "left":self.colour_left},
                   {"text":"Ball Speed", "func": ef, "surface":self.ball_speed_surface, 
                       "right":self.ball_speed_right, "left":self.ball_speed_left},
                   {"text":"Up:", "func": self.set_key, "var":"up_button",
                       "surface":self.key_surface},
                   {"text":"Down:", "func": self.set_key, "var":"down_button",
                       "surface":self.key_surface},
                   {"text":"Left:", "func": self.set_key, "var":"left_button",
                       "surface":self.key_surface},
                   {"text":"Right:", "func": self.set_key, "var":"right_button",
                       "surface":self.key_surface},
                   {"text":"Shoot ball:", "func": self.set_key, "var":"shoot_button",
                       "surface":self.key_surface},
                   {"text":"Pause:", "func": self.set_key, "var":"pause_button",
                       "surface":self.key_surface},
                   {"text":"Suicide:", "func": self.set_key, "var":"suicide_button",
                       "surface":self.key_surface},
                   {"text":"Save Settings", "func": self.exit_settings, "surface": None}]
        Menu_Scene.__init__(self, options)

class Main_Menu(Menu_Scene):
    def goto_settings(self):
        add_scene(Settings_Menu())
    def goto_highscore(self):
        add_scene(High_Score_View())
    def start_game(self):
        add_scene(Game_Scene(level=starting_level))

    def play_right(self):
        global starting_level
        if starting_level < unlocked_level:
            starting_level += 1
    def play_left(self):
        global starting_level
        if starting_level > 1:
            starting_level -= 1
    def play_surface(self):
        return self.arrow_surface("Play! (Lvl: " + str(starting_level) + ")")

    def __init__(self, selection=0):
        options = [{"text":"Play",       "func": self.start_game, "surface": self.play_surface, "right":self.play_right, "left":self.play_left},
                   {"text":"High Score", "func": self.goto_highscore, "surface": None},
                   {"text":"Settings",   "func": self.goto_settings, "surface": None},
                   {"text":"Exit",       "func": exit, "surface": None}]
        Menu_Scene.__init__(self, options)
        self.selection = selection

from ._Menu_Scene import _Menu_Scene

def ef(): pass

class Main_Menu(_Menu_Scene):
    def __init__(self):
        options = [{"text":"Play", "func": ef},
                   {"text":"High Score", "func": ef},
                   {"text":"Settings", "func": ef},
                   {"text":"Exit", "func": ef}]
        super().__init__(options)

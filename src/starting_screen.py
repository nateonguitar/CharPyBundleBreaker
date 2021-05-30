import datetime
import random

from charpy import GameObject, Matrix, Screen
import colorama
from pynput import keyboard

class StartingScreen(GameObject):
    def __init__(self):
        super().__init__()
        self.image = [
            '            Match 3               ',
            '   ---              ---           ',
            ' --   --          --   --         ',
            '-       -        -       -       -',
            '          --   --         --   -- ',
            '            ---             ---   ',
            '         Space to Start           ',
        ]
        self.randomize_colors()
        self.time_between_randomize = 0.1
        self.time_since_randomize = 0


    def randomize_colors(self):
        _image = []
        for i in range(len(self.image)):
            _list = list(self.image[i])
            _image.append([l if l != ' ' else None for l in _list])
        self.matrix = Matrix(_image)
        RED = colorama.Fore.RED
        GREEN = colorama.Fore.GREEN
        BLUE = colorama.Fore.BLUE
        YELLOW = colorama.Fore.YELLOW
        CYAN = colorama.Fore.CYAN
        MAGENTA = colorama.Fore.MAGENTA
        BRIGHT = colorama.Style.BRIGHT
        RESET_ALL = colorama.Style.RESET_ALL
        _colors = [
            lambda char :     f'{RED}{BRIGHT}{char}{RESET_ALL}',
            lambda char :   f'{GREEN}{BRIGHT}{char}{RESET_ALL}',
            lambda char :    f'{BLUE}{BRIGHT}{char}{RESET_ALL}',
            lambda char :  f'{YELLOW}{BRIGHT}{char}{RESET_ALL}',
            lambda char :    f'{CYAN}{BRIGHT}{char}{RESET_ALL}',
            lambda char : f'{MAGENTA}{BRIGHT}{char}{RESET_ALL}',
        ]
        for i in range(len(self.matrix)):
            row = self.matrix[i]
            for j in range(len(row)):
                if row[j] is None:
                    continue
                random_index = random.randint(0, len(_colors)-1)
                row[j] = _colors[random_index](row[j])


    def on_key_down(self, key: keyboard.Key):
        if key == keyboard.Key.space:
            self.game_instance.showing_starting_screen = False
            return


    def update(self, deltatime: datetime.timedelta):
        self.time_since_randomize += deltatime.total_seconds()
        if self.time_since_randomize >= self.time_between_randomize:
            self.time_since_randomize = 0
            self.randomize_colors()


    def draw(self, screen: Screen):
        screen.draw_matrix(self.matrix, self.position)

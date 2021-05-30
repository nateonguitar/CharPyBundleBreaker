import random

from charpy import GameObject, Matrix
import colorama
from pynput import keyboard

class StartingImage(GameObject):
    def __init__(self):
        super().__init__()
        self.image = [
            '   ---              ---           ',
            ' --   --          --   --         ',
            '-       -        -       -       -',
            '          --   --         --   -- ',
            '            ---             ---   ',
            '         Space to Start           ',
            '          x for random            ',
        ]
        
        self.randomize_colors()


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
        char = None
        if hasattr(key, 'char'):
            char = key.char
        if key == keyboard.Key.space:
            self.game_instance.showing_start_image = False
            return
        if char == 'x':
            self.randomize_colors()
            return
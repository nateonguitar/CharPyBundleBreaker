import random

from charpy import GameObject, Matrix, MatrixBorder, Vector2, Screen
import colorama

class Board(GameObject):
    

    def __init__(self, width:int, height:int):
        super().__init__()
        RED = colorama.Fore.RED
        GREEN = colorama.Fore.GREEN
        BLUE = colorama.Fore.BLUE
        YELLOW = colorama.Fore.YELLOW
        BRIGHT = colorama.Style.BRIGHT
        RESET_ALL = colorama.Style.RESET_ALL
        _RED    = lambda char :    f'{RED}{BRIGHT}{char}{RESET_ALL}'
        _GREEN  = lambda char :  f'{GREEN}{BRIGHT}{char}{RESET_ALL}'
        _BLUE   = lambda char :   f'{BLUE}{BRIGHT}{char}{RESET_ALL}'
        _YELLOW = lambda char : f'{YELLOW}{BRIGHT}{char}{RESET_ALL}'
        self.shapes = [
               _RED('♡'),
             _GREEN('♧'),
              _BLUE('♤'),
            _YELLOW('♢'),
        ]
        self.matrix = Matrix.empty_sized(height, width)
        self.position = Vector2(1, 1)
        self.fill()


    def draw(self, screen:Screen):
        screen.draw_matrix(self.matrix, self.position)


    def fill(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] != None:
                    continue
                random_index = random.randint(0,len(self.shapes)-1)
                self.matrix[i][j] = self.shapes[random_index]

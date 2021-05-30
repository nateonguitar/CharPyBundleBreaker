import datetime
import random

from pynput import keyboard
from charpy import GameObject, Matrix, Vector2, Screen
import colorama

from .cursor import Cursor

class GameBoard(GameObject):

    INSTRUCTIONS = {
        'position': Vector2.zero(),
        'matrix': Matrix([
            'Space or .     -> End turn            ',
            'Shift or /     -> Select piece to move',
            'WASD or Arrows -> Movement            ',
        ]),
    }

    def __init__(self):
        super().__init__()

        self.width = 8
        self.height = 8
        GameBoard.INSTRUCTIONS['position'].x = self.width + 3
        GameBoard.INSTRUCTIONS['position'].y = 3

        self.cursor = Cursor(Vector2(x=self.width, y=self.height))
        self.ending_turn = False
        self.end_turn_duration = 1
        self.time_since_ended_turn = 0

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
        self.matrix = Matrix.empty_sized(self.height, self.width)
        self.position = Vector2(1, 1)
        self.fill()


    def draw(self, screen:Screen):
        screen.draw_matrix(self.matrix, self.position)
        screen.draw_matrix(GameBoard.INSTRUCTIONS['matrix'], GameBoard.INSTRUCTIONS['position'])
        self.cursor.draw(screen)


    def fill(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] != None:
                    continue
                random_index = random.randint(0,len(self.shapes)-1)
                self.matrix[i][j] = self.shapes[random_index]


    def update(self, deltatime: datetime.timedelta):
        self.cursor.update(deltatime)
        if self.ending_turn:
            self.time_since_ended_turn += deltatime.total_seconds()
            if self.time_since_ended_turn >= self.end_turn_duration:
                self.time_since_ended_turn = 0
                self.ending_turn = False
                self.fill()


    def on_key_up(self, key: keyboard.Key):
        pass


    def on_key_down(self, key: keyboard.Key):
            self.cursor.on_key_down(key)
            char = None
            if hasattr(key, 'char'):
                char = key.char
            if char == '/' or key == keyboard.Key.shift:
                # TODO: handle selecting a piece to move
                pass
            if not self.ending_turn and (char == '.' or key == keyboard.Key.space):
                self.end_turn()
                return


    def end_turn(self):
        self.ending_turn = True
        m = self.matrix
        match_sizes = []
        for i in range(len(m)):
            for j in range(len(m[i])):
                char = m[i][j]
                if char is None:
                    continue
                down = 1
                right = 1
                # down
                for k in range(i+1, len(m)):
                    if m[k][j] is char:
                        down += 1
                    else:
                        break
                # right
                for k in range(j+1, len(m[i])):
                    if m[i][k] is char:
                        right += 1
                    else:
                        break
                scoring = down >= 3 or right >= 3
                if scoring:
                    if down > right:
                        match_sizes.append(down)
                        for k in range(i, i+down):
                            if m[k][j] is char:
                                m[k][j] = None
                    else:
                        match_sizes.append(right)
                        for k in range(j, j+right):
                            if m[i][k] is char:
                                m[i][k] = None

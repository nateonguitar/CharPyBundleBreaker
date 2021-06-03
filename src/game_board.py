import random

from pynput import keyboard
from charpy import GameObject, Matrix, Vector2, Screen
import colorama

from .cursor import Cursor
from .shape import Shape, HeartShape, ClubShape, SpadeShape, DiamondShape, BoxShape, OShape

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
        self.BRIGHT = colorama.Style.BRIGHT
        self.RESET_ALL = colorama.Style.RESET_ALL
        self.rows = 8
        self.columns = 8
        GameBoard.INSTRUCTIONS['position'].x = self.columns * 2 + 3
        GameBoard.INSTRUCTIONS['position'].y = 3
        self.cursor = Cursor(Vector2(x=self.columns, y=self.rows))
        self.ending_turn = False
        self.end_turn_duration = 1
        self.time_since_ended_turn = 0
        self.shapes = [
            HeartShape,
            ClubShape,
            SpadeShape,
            DiamondShape,
            BoxShape,
            OShape,
        ]
        self.matrix = Matrix.empty_sized(self.rows, self.columns)
        self.position = Vector2(1, 1)
        self.fill_spaces()
        self.matches: list[list[Vector2]] = self.detect_matches()
        self.display_matrix = self.generate_display_matrix()


    def draw(self, screen:Screen):
        screen.draw_matrix(self.display_matrix, self.position)
        screen.draw_matrix(GameBoard.INSTRUCTIONS['matrix'], GameBoard.INSTRUCTIONS['position'])
        self.cursor.draw(screen)


    def fill_spaces(self):
        size = self.size
        for i in range(0, size.y):
            for j in range(0, size.x):
                if self.matrix[i][j] != None:
                    continue
                random_index = random.randint(0,len(self.shapes)-1)
                RandomShapeClass = self.shapes[random_index]
                self.matrix[i][j] = RandomShapeClass()


    def generate_display_matrix(self) -> Matrix:
        columns = (self.columns * 2) - 1
        rows = (self.rows * 2) - 1
        m = Matrix.empty_sized(columns=columns, rows=rows)
        size = self.size
        for i in range(size.y):
            for j in range(size.x):
                shape = self.matrix[i][j]
                m[i*2][j*2] = f'{shape.color}{self.BRIGHT}{shape.char}{self.RESET_ALL}'
        for match in self.matches:
            first = match[0]
            second = match[1]
            color = self.matrix[first.y][first.x].color
            horizontal: bool = first.y == second.y
            for i in range(1, len(match)):
                if horizontal:
                    x = (first.x * 2) + (i * 2) - 1
                    y = (first.y * 2)
                    char = '-'
                else:
                    x = (first.x * 2)
                    y = (first.y * 2) + (i * 2) - 1
                    char = '|'
                m[y][x] = f'{color}{self.BRIGHT}{char}{self.RESET_ALL}'
        return m


    def update(self, deltatime: float):
        self.cursor.update(deltatime)
        if self.ending_turn:
            self.time_since_ended_turn += deltatime
            if self.time_since_ended_turn >= self.end_turn_duration:
                self.time_since_ended_turn = 0
                self.ending_turn = False
                self.fill_spaces()


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
        for row in self.matches:
            for node in row:
                self.matrix[node.y][node.x] = None


    def detect_matches(self) -> list[list[Vector2]]:
        size = self.size
        m = self.matrix
        matches = []
        for i in range(size.y):
            for j in range(size.x):
                shape: Shape = m[i][j]
                if shape is None:
                    continue
                char = shape.char
                down = 1
                right = 1
                # down
                for k in range(i+1, size.y):
                    if m[k][j] is None:
                        continue
                    next_shape: Shape = m[k][j]
                    if next_shape.char is char:
                        down += 1
                    else:
                        break
                # right
                for k in range(j+1, size.x):
                    if m[i][k] is None:
                        continue
                    next_shape: Shape = m[i][k]
                    if next_shape.char is char:
                        right += 1
                    else:
                        break
                scoring = down >= 3 or right >= 3
                if scoring:
                    nodes = []
                    if down > right:
                        for k in range(i, i+down):
                            nodes.append(Vector2(x=j, y=k))
                    else:
                        for k in range(j, j+right):
                            nodes.append(Vector2(x=k, y=i))
                    matches.append(nodes)
        return matches

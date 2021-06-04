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
            'Arrows or WASD -> Movement            ',
            'Space or .     -> Select piece to move',
            'Shift or /     -> End turn            ',
        ]),
    }

    def __init__(self):
        super().__init__()
        self.space_selected: Vector2 = None
        self.BRIGHT = colorama.Style.BRIGHT
        self.RESET_ALL = colorama.Style.RESET_ALL
        self.rows = 8
        self.columns = 8
        GameBoard.INSTRUCTIONS['position'].x = self.columns * 2 + 3
        GameBoard.INSTRUCTIONS['position'].y = 3
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
        self.cursor = Cursor(self)


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
                if shape is not None:
                    m[i*2][j*2] = f'{shape.color}{self.BRIGHT}{shape.char}{self.RESET_ALL}'
        for match in self.matches:
            first = match[0]
            second = match[1]
            first_shape = self.matrix[first.y][first.x]
            if first_shape is None:
                continue
            color = first_shape.color
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
        self.game_instance.debug_info['Cursor Position'] = self.cursor.position.__str__()


    def on_key_down(self, key: keyboard.Key):
        char = None
        if hasattr(key, 'char'):
            char = key.char
        if key == keyboard.Key.up or char == 'w':
            self.attempt_cursor_move('up')
            return
        if key == keyboard.Key.down or char == 's':
            self.attempt_cursor_move('down')
            return
        if key == keyboard.Key.left or char == 'a':
            self.attempt_cursor_move('left')
            return
        if key == keyboard.Key.right or char == 'd':
            self.attempt_cursor_move('right')
            return
        if key == keyboard.Key.space or char == '/':
            self.space_selected = not self.space_selected
            return
        if key == keyboard.Key.shift or char == '.':
            self.end_turn()
            return


    def attempt_cursor_move(self, direction: str):
        before_pos: Vector2 = self.cursor.position.clone()
        moved: bool = self.cursor.move(direction)
        if moved and self.space_selected == True:
            after_pos: Vector2 = self.cursor.position.clone()
            before_shape: Shape = self.matrix[before_pos.y][before_pos.x]
            after_shape: Shape = self.matrix[after_pos.y][after_pos.x]
            self.matrix[after_pos.y][after_pos.x] = before_shape
            self.matrix[before_pos.y][before_pos.x] = after_shape
            self.matches: list[list[Vector2]] = self.detect_matches()
            self.display_matrix = self.generate_display_matrix()
            # self.space_selected = False


    def on_key_up(self, key: keyboard.Key):
        pass


    def end_turn(self):
        for row in self.matches:
            for node in row:
                self.matrix[node.y][node.x] = None
        self.fill_spaces()
        self.matches = self.detect_matches()
        self.display_matrix = self.generate_display_matrix()


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
                if down >= 3:
                    nodes = []
                    for k in range(i, i+down):
                        nodes.append(Vector2(x=j, y=k))
                    matches.append(nodes)
                if right >= 3:
                    nodes = []
                    for k in range(j, j+right):
                        nodes.append(Vector2(x=k, y=i))
                    matches.append(nodes)
        return matches

import datetime

from charpy import GameObject, Matrix, MatrixBorder, Screen, Vector2
import colorama
from pynput import keyboard


class Cursor(GameObject):

    def __init__(self, game_board):
        super().__init__()
        self.game_board = game_board
        self.board_size = game_board.size

        self.matrix = Matrix \
            .empty_sized(rows=3, columns=3) \
            .with_border(border=MatrixBorder(MatrixBorder.DOUBLE_LINE))
        self.piece_selected_matrix = Matrix \
            .empty_sized(rows=3, columns=3) \
            .with_border(border=MatrixBorder(MatrixBorder.STARS))


    def draw(self, screen:Screen):
        position = self.position.clone()
        position.x *= 2
        position.y *= 2
        if self.game_board.selected_piece is None:
            screen.draw_matrix(self.matrix, position)
        else:
            screen.draw_matrix(self.piece_selected_matrix, position)


    def move(self, direction:str):
        position_before_move = self.position.clone()
        if direction == 'up':
            self.position.y = max(0, self.position.y-1)
        elif direction == 'down':
            self.position.y = min(self.board_size.y-1, self.position.y+1)
        elif direction == 'left':
            self.position.x = max(0, self.position.x-1)
        elif direction == 'right':
            self.position.x = min(self.board_size.x-1, self.position.x+1)
        moved = position_before_move.x != self.position.x
        moved = moved or position_before_move.y != self.position.y
        if moved:
            self.time_since_hide_matrix = 0
            self.hiding = False


    def on_key_down(self, key: keyboard.Key):
        char = None
        if hasattr(key, 'char'):
            char = key.char
        if char == 'w' or key == keyboard.Key.up:
            self.move('up')
            return
        if char == 's' or key == keyboard.Key.down:
            self.move('down')
            return
        if char == 'a' or key == keyboard.Key.left:
            self.move('left')
            return
        if char == 'd' or key == keyboard.Key.right:
            self.move('right')
            return

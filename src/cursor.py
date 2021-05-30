import datetime

from charpy import GameObject, Matrix, Screen, Vector2
import colorama
from pynput import keyboard


class Cursor(GameObject):

    def __init__(self, board_size: Vector2):
        """
        _game is a reference to the 
        """

        # bright
        _b = lambda char: f'{colorama.Style.BRIGHT}{char}{colorama.Style.RESET_ALL}'

        super().__init__()
        self.spin = False

        self.board_size = board_size
        self.state_index = 0

        self.matrix = Matrix((
            (None,    _b('↓'), None   ),
            (_b('→'), None,    _b('←')),
            (None,    _b('↑'), None   ),
        ))
        self.hiding = False
        self.hide_matrix_time = 0.2
        self.time_since_hide_matrix = 0

        self.spin_states = [
            Matrix((
                (None, _b('↓'), None),
                (None, None,    None),
                (None, _b('↑'), None),
            )),
            Matrix((
                (None,    None, _b('↙')),
                (None,    None, None   ),
                (_b('↗'), None, None   ),
            )),
            Matrix((
                (None,    None, None   ),
                (_b('→'), None, _b('←')),
                (None,    None, None   ),
            )),
            Matrix((
                (_b('↘'), None, None   ),
                (None,    None, None   ),
                (None,    None, _b('↖')),
            )),
        ]
        self.time_between_spin_states = 0.1
        self.time_since_spin_state_switch = 0


    def update(self, deltatime:datetime.timedelta):
        if self.spin:
            self.time_since_spin_state_switch += deltatime.total_seconds()
            if self.time_since_spin_state_switch >= self.time_between_spin_states:
                self.time_since_spin_state_switch = 0
                self.state_index += 1
                if self.state_index >= len(self.spin_states):
                    self.state_index = 0
        else:
            self.time_since_hide_matrix += deltatime.total_seconds()
            if self.time_since_hide_matrix >= self.hide_matrix_time:
                self.time_since_hide_matrix = 0
                self.hiding = not self.hiding


    def draw(self, screen:Screen):
        if self.spin:
            screen.draw_matrix(self.spin_states[self.state_index], self.position)
        else:
            if not self.hiding:
                screen.draw_matrix(self.matrix, self.position)


    def move(self, direction:str):
        position_before_move = None
        if not self.spin:
            position_before_move = self.position.clone()
        if direction == 'up':
            self.position.y = max(0, self.position.y-1)
        elif direction == 'down':
            self.position.y = min(self.board_size.y-1, self.position.y+1)
        elif direction == 'left':
            self.position.x = max(0, self.position.x-1)
        elif direction == 'right':
            self.position.x = min(self.board_size.x-1, self.position.x+1)
        if not self.spin:
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

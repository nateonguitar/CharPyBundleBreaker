import datetime

from charpy import Game, Matrix, Vector2
from pynput import keyboard

from .board import Board
from .cursor import Cursor
from .starting_image import StartingImage

class Match3Game(Game):

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
        self.showing_start_image = True
        Match3Game.INSTRUCTIONS['position'].x = self.width + 3
        Match3Game.INSTRUCTIONS['position'].y = 3
        self.board = Board()
        self.cursor = Cursor()
        self.starting_image = StartingImage()
        self.set_on_keydown(self.on_key_down)
        self.ending_turn = False
        self.end_turn_duration = 1
        self.time_since_ended_turn = 0

    def update(self, deltatime: datetime.timedelta):
        self.cursor.update(deltatime)
        if self.ending_turn:
            self.time_since_ended_turn += deltatime.total_seconds()
            if self.time_since_ended_turn >= self.end_turn_duration:
                self.time_since_ended_turn = 0
                self.ending_turn = False
                self.board.fill()


    def draw(self):
        if self.showing_start_image:
            self.screen.draw_matrix(self.starting_image.matrix, self.starting_image.position)
            super().draw()
            return
        self.board.draw(self.screen)
        self.cursor.draw(self.screen)
        self.screen.draw_matrix(Match3Game.INSTRUCTIONS['matrix'], Match3Game.INSTRUCTIONS['position'])
        super().draw()


    def on_key_down(self, key: keyboard.Key):
        if key == keyboard.Key.esc:
            self.end_game()
            return
        if self.showing_start_image:
            self.starting_image.on_key_down(key)
        else:
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
        m = self.board.matrix
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

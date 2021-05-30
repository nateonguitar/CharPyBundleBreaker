import datetime

from charpy import Game
from pynput import keyboard

from .board import Board
from .cursor import Cursor

class Match3Game(Game):

    def __init__(self):
        super().__init__()
        self.width = 8
        self.height = 8
        self.board = Board()
        self.cursor = Cursor()
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
        self.board.draw(self.screen)
        self.cursor.draw(self.screen)
        super().draw()


    def on_key_down(self, key:keyboard.Key):
        char = hasattr(key, 'char')
        if char:
            if key.char is 'w' or key == keyboard.Key.up:
                self.cursor.move('up')
                return
            if key.char is 's' or key == keyboard.Key.down:
                self.cursor.move('down')
                return
            if key.char is 'a' or key == keyboard.Key.left:
                self.cursor.move('left')
                return
            if key.char is 'd' or key == keyboard.Key.right:
                self.cursor.move('right')
                return
        else:
            if key == keyboard.Key.esc:
                self.end_game()
                return
            if key == keyboard.Key.space and not self.ending_turn:
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

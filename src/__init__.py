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
        self.board = Board(width=self.width, height=self.height)
        self.cursor = Cursor(self.board.size)
        self.set_on_keydown(self.on_key_down)


    def update(self, deltatime: datetime.timedelta):
        self.cursor.update(deltatime)


    def draw(self):
        self.board.draw(self.screen)
        self.cursor.draw(self.screen)
        super().draw()


    def on_key_down(self, key:keyboard.Key):
        if key == keyboard.Key.esc:
            self.end_game()
            return
        key_character = None
        try:
            key_character = key.char
        except:
            pass
        if key_character is 'w' or key == keyboard.Key.up:
            self.cursor.move('up')
            return
        if key_character is 's' or key == keyboard.Key.down:
            self.cursor.move('down')
            return
        if key_character is 'a' or key == keyboard.Key.left:
            self.cursor.move('left')
            return
        if key_character is 'd' or key == keyboard.Key.right:
            self.cursor.move('right')
            return

        if key == keyboard.Key.space:
            self.end_turn()
            return

    def end_turn(self):
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
        self.board.fill()

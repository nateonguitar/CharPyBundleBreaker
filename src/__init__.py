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
        if key_character == 'w' or key == keyboard.Key.up:
            self.cursor.move('up')
            return
        if key_character == 's' or key == keyboard.Key.down:
            self.cursor.move('down')
            return
        if key_character == 'a' or key == keyboard.Key.left:
            self.cursor.move('left')
            return
        if key_character == 'd' or key == keyboard.Key.right:
            self.cursor.move('right')
            return

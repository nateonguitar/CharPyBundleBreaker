import datetime

from charpy import Game
from pynput import keyboard

from .game_board import GameBoard
from .start_screen import StartScreen
from .count_down import CountDown

class Match3Game(Game):
    """
    This class is just the handler for the different screens.
    If the StartScreen is active it passes keystrokes and draw functions to that page.
    If the GameBoard is active, the same.
    """

    def __init__(self):
        super().__init__()
        self.set_on_keydown(self.on_key_down)
        self.set_on_keyup(self.on_key_up)
        self.start_screen = StartScreen()
        self.count_down: CountDown = None
        self.game_board: GameBoard = None
        # self.show_debug_info = True


    def update(self, deltatime: float):
        if self.start_screen is not None:
            self.start_screen.update(deltatime)
        if self.count_down is not None:
            self.count_down.update(deltatime)
        if self.game_board is not None:
            self.game_board.update(deltatime)


    def draw(self):
        if self.start_screen is not None:
            self.start_screen.draw(self.screen)
        if self.count_down is not None:
            self.count_down.draw(self.screen)
        if self.game_board is not None:
            self.game_board.draw(self.screen)
        super().draw()


    def on_key_down(self, key: keyboard.Key):
        if key == keyboard.Key.esc:
            self.end_game()
            return
        if self.start_screen is not None:
            self.start_screen.on_key_down(key)
        if self.game_board is not None:
            self.game_board.on_key_down(key)


    def on_key_up(self, key: keyboard.Key):
        if self.start_screen is not None:
            self.start_screen.on_key_up(key)
        if self.game_board is not None:
            self.game_board.on_key_up(key)


    def start_count_down(self):
        self.start_screen = None
        self.count_down = CountDown()


    def start_game(self):
        self.count_down = None
        self.game_board = GameBoard()

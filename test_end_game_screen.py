"""
Run this to generate a snapshot of the game and make sure all of the scoring / matching works.
This allows pdb break points without the game loop getting in the way.
Almost like a unit test, but you have to manually look at the output file and verify.
"""
from charpy import ConsolePrinter
from src.end_game_screen import EndGameScreen

printer = ConsolePrinter()
printer.clear_screen()
screen = printer.get_empty_screen()
scores = [
    1234,
    23456,
    123,
    6850,
]
e = EndGameScreen(scores)
e.draw(screen)
printer.draw_screen(screen)

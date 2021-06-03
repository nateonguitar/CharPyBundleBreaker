"""
Run this to generate a snapshot of the game and make sure all of the scoring / matching works.
This allows pdb break points without the game loop getting in the way.
Almost like a unit test, but you have to manually look at the output file and verify.
"""
from charpy import ConsolePrinter
from src.game_board import GameBoard
from src.shape import ClubShape, HeartShape

printer = ConsolePrinter()
printer.clear_screen()
screen = printer.get_empty_screen()

g = GameBoard()

g.cursor.move('down')
g.cursor.move('down')
g.cursor.move('down')
g.cursor.move('down')
g.cursor.move('down')
g.cursor.move('down')
g.cursor.move('down')
g.cursor.move('right')
g.cursor.move('right')
g.cursor.move('right')
g.cursor.move('right')
g.cursor.move('right')
g.cursor.move('right')
g.cursor.move('right')

g.matrix[0][3] = ClubShape()
g.matrix[0][4] = ClubShape()
g.matrix[0][5] = ClubShape()
g.matrix[2][3] = HeartShape()
g.matrix[3][3] = HeartShape()
g.matrix[4][3] = HeartShape()
g.matrix[5][3] = HeartShape()
g.matrix[3][2] = HeartShape()
g.matrix[3][3] = HeartShape()
g.matrix[3][4] = HeartShape()
g.matrix[3][5] = HeartShape()
g.matrix[4][2] = HeartShape()
g.matches = g.detect_matches()

g.display_matrix = g.generate_display_matrix()
g.draw(screen)
printer.draw_screen(screen)


with open('test_game_board.txt', 'w') as f:
    for row in g.matches:
        for node in row:
            f.write(f'(y={node.y}, x={node.x})')
        f.write("\n")

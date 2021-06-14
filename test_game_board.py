"""
Run this to generate a snapshot of the game and make sure all of the scoring / matching works.
This allows pdb break points without the game loop getting in the way.
Almost like a unit test, but you have to manually look at the output file and verify.
"""
from frolic import ConsolePrinter
from src.game_board import GameBoard
from src.shape import ClubShape, HeartShape

printer = ConsolePrinter()
printer.clear_screen()
screen = printer.get_empty_screen()

g = GameBoard()

g.matrix[0][0] = ClubShape()
g.matrix[0][1] = HeartShape()
g.matrix[0][2] = ClubShape()
g.matrix[0][3] = ClubShape()
g.matrix[0][4] = HeartShape()
g.matrix[1][0] = HeartShape()
g.matrix[1][1] = HeartShape()
g.matrix[1][2] = HeartShape()
g.matrix[1][3] = HeartShape()
g.matches = g.detect_matches()

g.space_selected = True

g.attempt_cursor_move('right')
g.matches = g.detect_matches()


# g.end_turn()
g.display_matrix = g.generate_display_matrix()
g.draw(screen)
printer.draw_screen(screen)



with open('test_game_board.txt', 'w') as f:
    for row in g.matches:
        for node in row:
            f.write(f'(y={node.y}, x={node.x})')
        f.write("\n")

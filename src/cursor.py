from frolic import GameObject, Matrix, MatrixBorder, Screen, Vector2

class Cursor(GameObject):

    def __init__(self, game_board):
        super().__init__()
        self.game_board = game_board
        self.board_size = game_board.size

        border = MatrixBorder(MatrixBorder.SINGLE_LINE_THIN)
        self.matrix: Matrix = Matrix \
            .empty_sized(rows=3, columns=3) \
            .with_border(border)
        self.matrix[0][1] = None
        self.matrix[1][0] = None
        self.matrix[1][2] = None
        self.matrix[2][1] = None
        border = MatrixBorder(MatrixBorder.DOUBLE_LINE)
        self.piece_selected_matrix = Matrix \
            .empty_sized(rows=3, columns=3) \
            .with_border(border)
        self.piece_selected_matrix[0][1] = None
        self.piece_selected_matrix[1][0] = None
        self.piece_selected_matrix[1][2] = None
        self.piece_selected_matrix[2][1] = None


    def draw(self, screen:Screen):
        position = self.position.add(Vector2(self.position.x, self.position.y))
        if self.game_board.space_selected:
            screen.draw_matrix(self.piece_selected_matrix, position)
        else:
            screen.draw_matrix(self.matrix, position)


    def move(self, direction:str) -> bool:
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
        return moved


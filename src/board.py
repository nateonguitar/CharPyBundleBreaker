import random

from charpy import GameObject, Matrix, MatrixBorder, Vector2, Screen

class Board(GameObject):


    def __init__(self, width:int, height:int):
        super().__init__()

        self.shapes = [
            '♤',
            '♡',
            '♧',
            '♢',
        ]

        self.matrix = Matrix.empty_sized(height, width)
        self.position = Vector2(1, 1)

        self.border_matrix_position = Vector2.zero()
        self.border_matrix = Matrix \
            .empty_sized(height+2, width+2) \
            .with_border(MatrixBorder(MatrixBorder.SINGLE_LINE_THIN))

        self.fill()


    def draw(self, screen:Screen):
        screen.draw_matrix(self.border_matrix, self.border_matrix_position)
        screen.draw_matrix(self.matrix, self.position)


    def fill(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] != None:
                    continue
                random_index = random.randint(0,len(self.shapes)-1)
                self.matrix[i][j] = self.shapes[random_index]

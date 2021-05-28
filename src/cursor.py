import datetime

from charpy import GameObject, Matrix, MatrixBorder, Vector2, Screen

class Cursor(GameObject):

    def __init__(self, board_size:Vector2):
        super().__init__()
        _border_char = '+'
        _border = MatrixBorder({
            'top': _border_char,
            'top_left': None,
            'top_right': None,
            'left': _border_char,
            'right': _border_char,
            'bottom': _border_char,
            'bottom_left': None,
            'bottom_right': None,
        })
        
        _border = MatrixBorder({
            'top': None,
            'top_left': '╝',
            'top_right': '╚',
            'left': None,
            'right': None,
            'bottom': None,
            'bottom_left': '╗',
            'bottom_right': '╔',
        })
        
        _border = MatrixBorder({
            'top': None,
            'top_left': '┘',
            'top_right': '└',
            'left': None,
            'right': None,
            'bottom': None,
            'bottom_left': '┐',
            'bottom_right': '┌',
        })
        
        _border = MatrixBorder({
            'top': '⯆',
            'top_left': None,
            'top_right': None,
            'left': '⯈',
            'right': '⯇',
            'bottom': '⯅',
            'bottom_left': None,
            'bottom_right': None,
        })
        
        _border = MatrixBorder({
            'top': '⮟',
            'top_left': None,
            'top_right': None,
            'left': '⮞',
            'right': '⮜',
            'bottom': '⮜',
            'bottom_left': None,
            'bottom_right': None,
        })
        self.matrix = Matrix.empty_sized(3, 3, None).with_border(_border)
        self.board_size = board_size
        self.visible = True
        self.visible_duration = 0.25
        self.visible_time_since_switch = 0


    def update(self, deltatime:datetime.timedelta):
        self.visible_time_since_switch += deltatime.total_seconds()
        if self.visible_time_since_switch >= self.visible_duration:
            self.visible_time_since_switch = 0
            self.visible = not self.visible


    def draw(self, screen:Screen):
        if not self.visible:
            return
        screen.draw_matrix(self.matrix, self.position)

    def move(self, direction:str):
        previous_position = self.position.clone()
        if direction == 'up':
            self.position.y = max(0, self.position.y-1)
        elif direction == 'down':
            self.position.y = min(self.board_size.y-1, self.position.y+1)
        elif direction == 'left':
            self.position.x = max(0, self.position.x-1)
        elif direction == 'right':
            self.position.x = min(self.board_size.x-1, self.position.x+1)
        moved = previous_position.x != self.position.x or previous_position.y != self.position.y
        if moved:
            self.visible = True
            self.visible_time_since_switch = 0

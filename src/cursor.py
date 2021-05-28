import datetime

from charpy import GameObject, Matrix, Vector2, Screen

class Cursor(GameObject):

    def __init__(self, board_size:Vector2):
        super().__init__()
        self.state_index = 0
        self.states = [
            Matrix((
                (None, '↓', None),
                (None, None, None),
                (None, '↑', None),
            )),
            Matrix((
                (None, None, '↙'),
                (None, None, None),
                ('↗', None, None),
            )),
            Matrix((
                (None, None, None),
                ('→', None, '←'),
                (None, None, None),
            )),
            Matrix((
                ('↘', None, None),
                (None, None, None),
                (None, None, '↖'),
            )),
        ]
        self.board_size = board_size
        self.time_between_states = 0.1
        self.time_since_state_switch = 0


    def update(self, deltatime:datetime.timedelta):
        self.time_since_state_switch += deltatime.total_seconds()
        if self.time_since_state_switch >= self.time_between_states:
            self.time_since_state_switch = 0
            self.state_index += 1
            if self.state_index >= len(self.states):
                self.state_index = 0



    def draw(self, screen:Screen):
        screen.draw_matrix(self.states[self.state_index], self.position)

    def move(self, direction:str):
        if direction == 'up':
            self.position.y = max(0, self.position.y-1)
        elif direction == 'down':
            self.position.y = min(self.board_size.y-1, self.position.y+1)
        elif direction == 'left':
            self.position.x = max(0, self.position.x-1)
        elif direction == 'right':
            self.position.x = min(self.board_size.x-1, self.position.x+1)

from frolic import GameObject, Matrix, Screen, Vector2


class CountDown(GameObject):
    def __init__(self):
        super().__init__()
        self.time_since_tick = 0
        self.time_between_ticks = 1
        self.tick = 3
        char = '█'
        self.ticks = [
            Matrix([
                [None, None, char, char, None, None,],
                [None, char, char, char, None, None,],
                [None, None, char, char, None, None,],
                [None, None, char, char, None, None,],
                [None, None, char, char, None, None,],
                [None, None, char, char, None, None,],
                [None, char, char, char, char, None,],
            ]),
            Matrix([
                [None, char, char, char, char, None,],
                [char, char, None, None, char, char,],
                [None, None, None, None, char, char,],
                [None, None, char, char, char, None,],
                [None, char, char, None, None, None,],
                [char, char, None, None, None, None,],
                [char, char, char, char, char, char,],
            ]),
            Matrix([
                [None, char, char, char, char, None,],
                [char, char, None, None, char, char,],
                [None, None, None, None, char, char,],
                [None, None, char, char, char, None,],
                [None, None, None, None, char, char,],
                [char, char, None, None, char, char,],
                [None, char, char, char, char, None,],
            ]),
        ]


    def update(self, deltatime: float):
        self.time_since_tick += deltatime
        if self.time_since_tick >= self.time_between_ticks:
            self.time_since_tick = self.time_between_ticks - self.time_since_tick
            self.tick -= 1
            if self.tick == 0:
                self.game_instance.start_game()


    def draw(self, screen: Screen):
        screen.draw_matrix(self.ticks[self.tick-1], Vector2(4, 1))

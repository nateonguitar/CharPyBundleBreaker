from charpy import Game

class Match3Game(Game):
    def __init__(self):
        super().__init__()

    def update(self, deltatime):
        pass

    def draw(self):
        self.screen.set(3, 3, 'X')
        super().draw()

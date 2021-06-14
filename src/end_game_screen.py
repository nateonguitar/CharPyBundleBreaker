from frolic import GameObject, Screen, Vector2
from pynput import keyboard

class EndGameScreen(GameObject):

    def __init__(self, scores: list[int]):
        self.scores = scores


    def update(self, deltatime: float):
        pass


    def draw(self, screen: Screen):
        screen.draw_string('GAME OVER', Vector2(9, 1))
        screen.draw_string('Space to try again', Vector2(4, 3))
        scores_offset = Vector2(10, 5)
        screen.draw_string('Scores', scores_offset)
        screen.draw_string('--------', scores_offset.add(Vector2(-1, 1)))
        for i in range(len(self.scores)):
            score = self.scores[i]
            string = f'{i+1}: {score}'
            pos = scores_offset.add(Vector2(-1, i+2))
            screen.draw_string(string, pos)


    def on_key_down(self, key: keyboard.Key):
        if key == keyboard.Key.space:
            self.game_instance.restart()

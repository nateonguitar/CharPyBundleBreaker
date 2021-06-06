from charpy import GameObject, Screen, Vector2
from pynput import keyboard

class EndGameScreen(GameObject):

    def __init__(self, scores: list[int]):
        self.scores = scores


    def update(self, deltatime: float):
        pass


    def draw(self, screen: Screen):
        screen.draw_string(f'         GAME OVER', Vector2(0, 1))
        screen.draw_string(f'    Space to try again', Vector2(0, 3))
        score_offset = Vector2(10, 5)
        screen.draw_string('Scores', score_offset)
        screen.draw_string('--------', score_offset.add(Vector2(-1, 1)))
        for i in range(len(self.scores)):
            score = self.scores[i]
            screen.draw_string(f'{i+1}: {score}', score_offset.add(Vector2(-1, i+2)))


    def on_key_down(self, key: keyboard.Key):
        if key == keyboard.Key.space:
            self.game_instance.restart()

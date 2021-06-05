from charpy import GameObject, Screen, Vector2
from pynput import keyboard

class EndGameScreen(GameObject):

    def __init__(self, score: int):
        self.score = score


    def update(self, deltatime: float):
        pass


    def draw(self, screen: Screen):
        screen.draw_string(f'         GAME OVER', Vector2(x=0, y=1))
        screen.draw_string(f'    Space to try again', Vector2(x=0, y=3))
        screen.draw_string(f'       Score: {self.score}', Vector2(x=0, y=7))


    def on_key_down(self, key: keyboard.Key):
        if key == keyboard.Key.space:
            self.game_instance.restart()

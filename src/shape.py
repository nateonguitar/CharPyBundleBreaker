from colorama import Fore

class Shape():
    def __init__(self, char: str, color: int):
        self.char = char
        self.color = color

class HeartShape(Shape):
    def __init__(self):
        super().__init__(char='♥', color=Fore.RED)

class ClubShape(Shape):
    def __init__(self):
        super().__init__(char='♠', color=Fore.GREEN)

class SpadeShape(Shape):
    def __init__(self):
        super().__init__(char='♣', color=Fore.BLUE)

class DiamondShape(Shape):
    def __init__(self):
        super().__init__(char='♦', color=Fore.YELLOW)

class BoxShape(Shape):
    def __init__(self):
        super().__init__(char='■', color=Fore.CYAN)

class OShape(Shape):
    def __init__(self):
        super().__init__(char='◖', color=Fore.MAGENTA)

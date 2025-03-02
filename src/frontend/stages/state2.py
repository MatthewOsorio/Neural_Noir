from backend.BackendInterface.GameManager import GameManager

class State2:
    def __init__(self):
        self.game = None
        print("State")
    
    def setGame(self, game):
        self.game = game

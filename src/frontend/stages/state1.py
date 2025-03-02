from backend.BackendInterface.GameManager import GameManager

class State1:
    def __init__(self):
        self.game = None
        self.state = None
        self.response = None

        self.heartRate = []
        self.temperature = []
        self.eda = []

    def setGame(self, game):
        self.game = game
    
    def begin(self):
        self.game._gameState.updateState(1)
        self.response = self.game.generateAIResponse()
        return self.response
        
    def convert(self):
        self.game.convertTTS(self.response)
    
    def generateResponse(self):
        self.response = self.game.generateAIResponse()
        return self.response

    def updateData(self):
        pass
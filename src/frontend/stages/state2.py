from backend.BackendInterface.GameManager import GameManager

#Feel free to change this class as needed. 
class State2:
    def __init__(self):
        self.game = None
        self.state = None
        self.response = None
        self.endPhase = False
    
    def setGame(self, game):
        self.game = game

    def begin(self):
        self.game._gameState.updateState(2)
        self.response = self.introduceEvidence()
        return self.response
        
    def convert(self):
        self.game.convertTTS(self.response)
    
    def generateResponse(self):
        print("Generating response")
        self.response = self.game.generateAIResponse()

        if self.response == False:
            print("Ending phase")
            self.endPhase = True

        return self.response
    
    def introduceEvidence(self):
        self.game._aiController.introduceEvidence()

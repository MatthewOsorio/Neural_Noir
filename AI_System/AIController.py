from GameState import GameState 
from .AI_Behavior import AI_InitialPhase, AI_EarlyInterrogation, AI_MidInterrogation, AI_FinalInterrogation, AIContext

class AIController:
    def __init__(self, gameStateObject):
        self.gameState = gameStateObject
        self.ai = None        

    def setAIBehavior(self):
        match self.gameState.getState():
            case GameState.initialPhase.value:
                self.ai = AIContext(AI_InitialPhase(self.conversation))
            # case GameState.first_interrogation.value:
            #     self.ai = AIContext(AI_EarlyInterrogation(self.))
            # case GameState.second_interrogation.value:
            #     self.ai = AIContext.AIBehavior()

    def generateResponse(self):
        return self.ai.generateResponse()
    # generete responses based on state
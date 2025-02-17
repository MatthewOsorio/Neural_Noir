from GameState import GameState 
from AI_Behavior import AI_InitialPhase, AI_MidInterrogation, AI_FinalInterrogation, AIContext
from ConversationModel import ConversationModel

class AIController:
    def __init__(self):
        self.gameState = None
        self.ai = None        

    def setAIBehavior(self):
        match self.gameState:
            case GameState.initialPhase.value:
                self.ai = AIContext(AI_InitialPhase(self.conversation))
            # case GameState.first_interrogation.value:
            #     self.ai = AI_Context(AIFirstHalfGameState.AIFirstHalfGameState())
            # case GameState.second_interrogation.value:
            #     self.ai = AI_Context.AIBehavior()

    def generateResponse(self):
        return self.ai.generateResponse()
    # generete responses based on state
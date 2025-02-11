from GameState import GameState 
from AI_Behavior import AI_InitialPhase, AI_MidInterrogation, AI_FinalInterrogation, AI_Context
from ConversationModel import ConversationModel

class AIController:
    def __init__(self):
        self.gameState = None
        self.ai = None
        self.conversation = ConversationModel()
        
    def setGameState(self, state):
        self.gameState = state
        self.setAIBehavior()

    def setAIBehavior(self):
        match self.gameState:
            case GameState.initialPhase.value:
                self.ai = AI_Context(AI_InitialPhase(self.conversation))
            # case GameState.first_interrogation.value:
            #     self.ai = AI_Context(AIFirstHalfGameState.AIFirstHalfGameState())
            # case GameState.second_interrogation.value:
            #     self.ai = AI_Context.AIBehavior()

    def generateResponse(self):
        return self.ai.generateResponse()
    # generete responses based on state
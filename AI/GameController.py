from GameState import GameState 
from AI import AIBehavior
from AI import AIEarlyGameState
from AI import AIFirstHalfGameState
from AI import AISecondHalfGameState


class GameController:
    def __init__(self):
        self.gameState = None
        self.ai = None
        
    def setGameState(self, state):
        self.gameState = state
        self.setAIBehavior()

    def setAIBehavior(self):
        match self.gameState:
            case GameState.basic_questioning.value:
                self.ai = AIBehavior.AIBehavior(AIEarlyGameState.AIEarlyGameState())
            case GameState.first_interrogation.value:
                self.ai = AIBehavior.AIBehavior(AIFirstHalfGameState.AIFirstHalfGameState())
            case GameState.second_interrogation.value:
                self.ai = AIBehavior.AIBehavior()

    def generateResponse(self):
        pass
    # generete responses based on state
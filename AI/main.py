from AIController import AIController
from ConversationModel import ConversationModel
from GameState import GameState

ai = AIController()
ai.setGameState(1)


response = ai.generateResponse()
print(response)
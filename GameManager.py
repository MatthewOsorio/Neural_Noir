from AI_System import AIController
from GameStateManager import GameStateManager
from ConversationModel import ConversationModel

gameState = GameStateManager()
conversation = ConversationModel()
ai = AIController.AIController(conversation)
gameState.setAIReference(ai)
gameState.updateState(1)


while(True):
    ai_response = ai.generateResponse()
    conversation.addAIResponse(ai_response)
    print(ai_response)
    user_statement = input('> ')
    ai.processUserResponse(user_statement)


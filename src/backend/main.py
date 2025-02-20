# File for testing backend stuff
from AI_System import AIController
from backend.GameStateManager import GameStateManager
from backend.ConversationModel import ConversationModel

gameState = GameStateManager()
conversation = ConversationModel()
ai = AIController.AIController(conversation)
gameState.setAIReference(ai)
gameState.updateState(1)

finished_phase = False

while(not finished_phase):
    ai_response = ai.generateResponse()
    if ai_response == False:
        finished_phase = True
    else:
        conversation.addAIResponse(ai_response)
        print(ai_response)
        user_statement = input('> ')
        ai.processUserResponse(user_statement)


# File for testing backend stuff
from BackendInterface.GameManager import GameManager

gameState = GameManager()
gameState.setupGame(False)
gameState.updateGameState(3)
finished = False

while(not finished):
    ai_response = gameState.generateAIResponse()
    if ai_response == False:
        finished = True
    else:
        print(ai_response)
        user_statement = input('> ')
        gameState.processUserResponse(user_statement)

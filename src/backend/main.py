# File for testing backend stuff
from BackendInterface.GameManager import GameManager

gameState = GameManager()
gameState.setupGame(False)
gameState.updateGameState(1)
finished_phase1 = False
finished_phase2 = False
while(not finished_phase1):
    ai_response = gameState.generateAIResponse()
    if ai_response == False:
        gameState.updateGameState(2)
    else:
        print(ai_response)
        user_statement = input('> ')
        gameState.processUserResponse(user_statement)

gameState.updateGameState(2)

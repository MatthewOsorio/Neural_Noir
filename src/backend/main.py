# File for testing backend stuff
from BackendInterface.GameManager import GameManager

gameManager = GameManager()
gameManager.setupGame(False)
gameManager.updateGameState(2)
finished = False

while(not finished):
    ai_response = gameManager.generateAIResponse()
    print(ai_response)
    if ai_response == False:
        finished = True
    else:
        user_statement = input('> ')
        gameManager.processUserResponse(user_statement)

print(gameManager.getVerdictsFromDB(gameManager.getSessionID()))
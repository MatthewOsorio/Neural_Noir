from src.backend.BackendInterface.GameManager import GameManager

game = GameManager()

game.setupGame(False)
game.updateGameState(1)

finished = False

while not finished:
    response = game.generateAIResponse()

    if response:
        print(response)
        user_response = input('> ')
        game.processUserResponse(user_response)
    else:
        finished = True
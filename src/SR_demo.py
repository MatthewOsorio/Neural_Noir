# File for testing backend stuff
from backend.AI_System.AIController import AIController
from backend.GameStateSystem.GameStateManager import GameStateManager
from backend.Conversation.ConversationModel import ConversationModel
from backend.Database.DatabaseController import DatabaseController
from backend.Database.SessionController import SessionController
from backend.BackendInterface.GameManager import GameManager

# Initialize the database and the session
database = DatabaseController()
session = SessionController(database)
session.start()

# Initialize the game state and AI system
conversation = ConversationModel(database, session)
ai = AIController(conversation)

# Initialize game state and AI reference
gameState = GameStateManager()
gameState.setEmotibitUsed(False)
gameState.setAIReference(ai)
gameState.updateState(1)

# Intialize GameManager
gameManager = GameManager()
gameManager.setupGame(False)

finished_phase = False

while not finished_phase:
    ai_response = ai.generateResponse()
    if ai_response == False:
        finished_phase = True
    else:
        conversation.addAIResponse(ai_response)
        print(ai_response)
        # user_statement = input('> ') # In the final main.py, this is listenToUser() from GameManager
        user_statement = gameManager.listenToUser()
        ai.processUserResponse(user_statement)
        conversation.sendUserResponseToDB(session.startTime, None, user_statement)
        ai.processUserResponse(user_statement)

conversation_history = database.fetchConversation(session.getSessionID())
for user_input, response in conversation_history:
    print(f"User: {user_input}")
    print(f"AI: {response}")
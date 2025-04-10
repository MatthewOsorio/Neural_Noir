# File for testing backend stuff
from backend.AI_System.AIController import AIController
from backend.GameStateSystem.GameState import GameState
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

states = [
    GameState.initialPhase,
    GameState.earlyInterrogation,
    GameState.midInterrogation,
    GameState.finalInterrogation
]
state_index = 0
gameState.updateState(states[state_index])

while state_index < len(states):
    finished_phase = False

    while not finished_phase:
        ai_response = ai.generateResponse()
        if ai_response == False:
            finished_phase = True
            state_index += 1
            if state_index < len(states): 
                gameState.updateState(states[state_index])
                ai_response = ai.generateResponse()
                if ai_response:
                    print(ai_response)
        else:
            print(ai_response)
            user_input = input('> ')
            ai.processUserResponse(user_input)

# conversation_history = database.fetchConversation(session.getSessionID())
# for user_input, response in conversation_history:
#     print(f"User: {user_input}")
#     print(f"AI: {response}")
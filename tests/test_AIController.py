from .context import AIController
from .context import ConversationModel
from .context import GameState
from .context import GameStateManager
from .context import AIInitialPhase
from .context import AIEarlyInterrogation
from .context import AIMidInterrogation
from .context import AIFinalInterrogation
import pytest

@pytest.fixture
def conversation():
    return ConversationModel()

@pytest.fixture
def aiController(conversation):
    ai = AIController(conversation)
    return ai

@pytest.fixture
def gameStateManager():
    return GameStateManager()

@pytest.fixture
def gameState():
    game= GameStateManager()
    game.setEmotibitUsed(False)

    return game

#ensures the first question the AI asks is the correct question
def test_generate_response_with_first_question(aiController):
    aiController.update(GameState.initialPhase)
    first_question = aiController.generateResponse()

    assert first_question == "Harris: What is your name?"

# First question is What is your name? The correct answer is Mark Chadeten
# Because gpt deems the users response it be valid it will move on to the next question
def test_AI_respond_to_correct_answer(aiController):
    aiController.update(GameState.initialPhase)
    aiController.generateResponse()
    aiController.processUserResponse("My name is Mark Chadenten")

    assert aiController.generateResponse() == 'Harris: Do you work at the Reno Times?'

# First question is What is your name? The correct answer is Mark Chadeten
# Because gpt deems the users response wrong so it will not move on next question
# Gpt will return a different question, instructing the user to stop lying
def test_AI_respond_to_wrong_answer(aiController):
    aiController.update(GameState.initialPhase)

    aiController.generateResponse()
    aiController.processUserResponse("My name is Sara Le")

    assert aiController.generateResponse() != 'Harris: Do you work at the Reno Times'

# First question is What is your name? The correct answer is Mark Chadeten
# Because gpt deems the users response to not be valid so it will not move on next question
# Gpt will return a different question, instructing the user to stop messing aroun
def test_AI_respond_to_invalid_answer(aiController):
    aiController.update(GameState.initialPhase)

    aiController.generateResponse()
    aiController.processUserResponse("GET OUT OF MY HEAD, GET OUT OF MY HEAD")

    assert aiController.generateResponse() != 'Harris: Do you work at the Reno Times'

# Tests that the gamestate can hold a reference to the current ai controller
def test_AI_is_refernced_in_game_state_manager(aiController, gameState):
    gameState.setAIReference(aiController)

    assert gameState._aiReference == aiController

#Tests that when the game state updates the ai controller also updates the ai behavior automatically    
def test_AI_behavior_updates_when_game_state_upates(aiController, gameState):
    gameState.setAIReference(aiController)

    gameState.updateState(1)
    assert isinstance(aiController._ai._state, AIInitialPhase)

    gameState.updateState(2)
    assert isinstance(aiController._ai._state, AIEarlyInterrogation)

    gameState.updateState(3)
    assert isinstance(aiController._ai._state, AIMidInterrogation)

    gameState.updateState(4)
    assert isinstance(aiController._ai._state, AIFinalInterrogation)
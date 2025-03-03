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

def test_generate_response_with_first_question(aiController):
    aiController.update(GameState.initialPhase)
    first_question = aiController.generateResponse()

    assert first_question == "Harris: What is your name?"

def test_AI_respond_to_correct_answer(aiController):
    aiController.update(GameState.initialPhase)
   # First question is What is your name? The correct answer is Mark Chadeten
    aiController.generateResponse()
    aiController.processUserResponse("My name is Mark Chadenten")

    # Because gpt deems the users response it be valid it will move on to the next question
    assert aiController.generateResponse() == 'Harris: Do you work at the Reno Times?'

def test_AI_respond_to_wrong_answer(aiController):
    aiController.update(GameState.initialPhase)

    # First question is What is your name? The correct answer is Mark Chadeten
    aiController.generateResponse()
    aiController.processUserResponse("My name is Sara Le")

    # Because gpt deems the users response wrong so it will not move on next question
    # Gpt will return a different question, instructing the user to stop lying
    assert aiController.generateResponse() != 'Harris: Do you work at the Reno Times'


def test_AI_respond_to_invalid_answer(aiController):
    aiController.update(GameState.initialPhase)

    # First question is What is your name? The correct answer is Mark Chadeten
    aiController.generateResponse()
    aiController.processUserResponse("GET OUT OF MY HEAD, GET OUT OF MY HEAD")

    # Because gpt deems the users response to not be valid so it will not move on next question
    # Gpt will return a different question, instructing the user to stop messing around
    assert aiController.generateResponse() != 'Harris: Do you work at the Reno Times'

def test_AI_is_refernced_in_game_state_manager(aiController, gameState):
    gameState.setAIReference(aiController)

    assert gameState._aiReference == aiController

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
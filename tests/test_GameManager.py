import pytest
from .context import GameManager

@pytest.fixture
def game_manager():
    return GameManager()

def test_set_up(game_manager):
    game_manager.setupGame()
    
    assert game_manager._aiController != None
    assert game_manager._bioController != None
    assert game_manager._conversation != None
    assert game_manager._gameState != None
    assert game_manager._sr != None
    assert game_manager._tts != None
    assert game_manager._bioController._aiReference == game_manager._aiController
    assert game_manager._gameState._aiReference == game_manager._aiController
    assert game_manager._gameState._biometricReference == game_manager._bioController
    
def test_generateAIResponse(game_manager):
    game_manager.
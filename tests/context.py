import os
import sys

# Ensure the parent directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.backend.AI_System.AIController import AIController
from src.backend.AI_System.AI_Behavior.AI_InitialPhase import AIInitialPhase
from src.backend.AI_System.AI_Behavior.AI_EarlyInterrogation import AIEarlyInterrogation
from src.backend.AI_System.AI_Behavior.AI_MidInterrogation import AIMidInterrogation
from src.backend.AI_System.AI_Behavior.AI_FinalInterrogation import AIFinalInterrogation
from src.backend.BackendInterface.GameManager import GameManager
from src.backend.BiometricSystem.BiometricController import BiometricController
from src.backend.Conversation.ConversationModel import ConversationModel
from src.backend.SRSystem.SpeechToText import SpeechToText
from src.backend.TTSSystem import TextToSpeechController
from src.backend.Database.DatabaseController import DatabaseController
from src.backend.GameStateSystem.GameState import GameState
from src.backend.GameStateSystem.GameStateManager import GameStateManager
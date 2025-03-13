import os
import sys

# Ensure the parent directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.backend.AI_System.AIController import AIController
from src.backend.BackendInterface.GameManager import GameManager
from src.backend.BiometricSystem.BiometricController import BiometricController
from src.backend.Conversation.ConversationModel import ConversationModel
from src.backend.SRSystem.SpeechToText import SpeechToText
from src.backend.TTSSystem import TextToSpeechController
from src.backend.Database.DatabaseController import DatabaseController
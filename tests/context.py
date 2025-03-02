import os
import sys

# Ensure the parent directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from backend.AI_System.AIController import AIController
from backend.BackendInterface.GameManager import GameManager
from backend.BiometricSystem.BiometricController import BiometricController
from backend.Conversation.ConversationModel import ConversationModel
from backend.SRSystem.SpeechToText import SpeechToText
from backend.TTSSystem import TextToSpeechController
from backend.Database.Database import Database
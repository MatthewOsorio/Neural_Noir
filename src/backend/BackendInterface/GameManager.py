from AI_System import AIController
from BiometricSystem import BiometricController
from Conversation import ConversationModel
from GameStateSystem import GameStateManager
from SRSystem import SpeechToText
from TTSSystem import TextToSpeechController

class GameManager:
    def __init__(self):
        self._conversation = ConversationModel.ConversationModel()
        self._gameState = GameStateManager.GameStateManager()
        self._ai = AIController.AIController(self._conversation)
        self._gameState.setAIReference(self._ai)

        self._emotibit = BiometricController.BiometricController()
        self._emotibit.setAIReference(self._ai)
        self._sr = SpeechToText.SpeechToText()
        self._tts = TextToSpeechController()

    def generateAIResponse(self):
        # will implement this later
        pass

    def proceossUserResponse(self, response):
        # will implement this later
        pass

    def listenToUser(self):
        # will implement this later
        pass

    def getUserHeart(self):
        return self._emotibit.getHeartRate()

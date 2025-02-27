from ..AI_System.AIController import AIController
from ..BiometricSystem.BiometricController import BiometricController
from ..Conversation.ConversationModel import ConversationModel
from ..GameStateSystem.GameStateManager import GameStateManager
from ..SRSystem.SpeechToText import SpeechToText
from ..TTSSystem.TextToSpeechController import TextToSpeechController

class GameManager:
    def __init__(self):
        self._aiController = None
        self._bioController = None
        self._conversation = None
        self._gameState = None
        self._sr = None
        self._tts = None
        self._gameIsReady = False

    # instantiate all objects here
    def setupGame(self):
        self._conversation = ConversationModel()
        self._aiController = AIController(self._conversation)
        self._bioController = BiometricController()
        self._gameState = GameStateManager()
        self._sr = SpeechToText()
        self._tts = TextToSpeechController()

        self._gameState.setAIReference(self._aiController)
        self._gameState.setBiometricReference(self._bioController)
        self._bioController.setAIReferece(self._aiController)

        self._gameIsReady = True

    def generateAIResponse(self) -> str:
        if not self._gameIsReady:
            raise Exception("Game is not ready, please invoke setupGame() first")
        return self._aiController.generateResponse()
    
    def listenToUser(self):
        if not self._gameIsReady:
            raise Exception("Game is not ready, please invoke setupGame() first")
        
        responseAudio = self._sr.listen()
        responseText = self._sr.transcribe(responseAudio)
        
        #possibly spin another thread for the db
        self._conversation.sendUserResponseToDB(self._sr.getStartTime(), self._sr.getEndTime(), responseText)
        self.processUserResponse(responseText)

    def processUserResponse(self, user_response):
        if not self._gameIsReady:
            raise Exception("Game is not ready, please invoke setupGame() first")
        self._aiController.processUserResponse(user_response)

    def getUserHeartRate(self):
        if not self._gameIsReady:
            raise Exception("Game is not ready, please invoke setupGame() first") 
        
        return self._bioController.getHeartRate()
    
    def getUserTemperature(self):
        if not self._gameIsReady:
            raise Exception("Game is not ready, please invoke setupGame() first") 
        
        return self._bioController.getTemperature()
    
    def getUserEDA(self):
        if not self._gameIsReady:
            raise Exception("Game is not ready, please invoke setupGame() first") 
        
        return self._bioController.getEDA()
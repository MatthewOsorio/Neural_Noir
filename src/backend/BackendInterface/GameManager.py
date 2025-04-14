from AI_System.AIController import AIController
from BiometricSystem.BiometricController import BiometricController
from Conversation.ConversationModel import ConversationModel
from GameStateSystem.GameStateManager import GameStateManager
from SRSystem.SpeechToText import SpeechToText
from TTSSystem.TextToSpeechController import TextToSpeechController
from Database.DatabaseController import DatabaseController
from Database.SessionController import SessionController

class GameManager:
    def __init__(self):
        self._aiController = None
        self._bioController = None
        self._conversation = None
        self._gameState = None
        self._sr = None
        self._tts = None
        self._gameIsReady = False
        self._database = None
        self._sessionController = None
            
        self.response = None
        self.userResponse = None

        self._useEmotibit = False

    # instantiate all objects here
    def setupGame(self, emotibitUsed):
        self._database = DatabaseController()
        self._sessionController = SessionController(self._database)
        self._conversation = ConversationModel(self._database, self._sessionController)
        self._aiController = AIController(self._conversation)
        self._gameState = GameStateManager()
        self._sr = SpeechToText()
        self._tts = TextToSpeechController()
        self._gameState.setAIReference(self._aiController)
        
        self._sessionController.start()
    
        if emotibitUsed:
            self._gameState.setEmotibitUsed(True)
            self._bioController = BiometricController()
            self._bioController._gameIsReady = True
            self._gameState.setBiometricReference(self._bioController)
            self._bioController.setAIReferece(self._aiController)

        self._gameState.setEmotibitUsed(False)
        self._gameIsReady = True

    def generateAIResponse(self) -> str:
        if not self._gameIsReady:
            raise Exception("Game is not ready, please invoke setupGame() first")
        self.response = self._aiController.generateResponse()
        return self.response
    
    def listenToUser(self):
        if not self._gameIsReady:
            raise Exception("Game is not ready, please invoke setupGame() first")
        
        responseAudio = self._sr.listen()
        responseText = self._sr.transcribe(responseAudio)
        self.userResponse = responseText

        if responseText is None:
            print("Warning: No speech detected. Asking player to repeat.")
            responseText = "I didn't hear that, can you repeat?"
        
        #possibly spin another thread for the db
        #self._conversation.sendUserResponseToDB(self._sr.getStartTime(), self._sr.getEndTime(), responseText)
        self.processUserResponse(responseText)
        return responseText

    def processUserResponse(self, userResponse):
        if not self._gameIsReady:
            raise Exception("Game is not ready, please invoke setupGame() first")
        self._aiController.processUserResponse(userResponse)

    def getUserHeartRate(self):
        if not self._gameIsReady:
            raise Exception("Game is not ready, please invoke setupGame() first") 
        elif not self._useEmotibit:
            return None
        return self._bioController.getHeartRate()
    
    def updateGameState(self, state):
        self._gameState.updateState(state)

    def getUserTemperature(self):
        if not self._gameIsReady:
            raise Exception("Game is not ready, please invoke setupGame() first") 
        elif not self._useEmotibit:
            return None
        return self._bioController.getTemperature()
    
    def getUserEDA(self):
        if not self._gameIsReady:
            raise Exception("Game is not ready, please invoke setupGame() first") 
        elif not self._useEmotibit:
            return None        
        return self._bioController.getEDA()
    
    def setRanges(self, rangeH, rangeE, rangeT):
        if not self._gameIsReady:
            raise Exception("Game is not ready, please invoke setupGame() first") 
        elif not self._useEmotibit:
            return None
        
        self._bioController.biometricReader.heartRateBase = rangeH
        self._bioController.biometricReader.edaBase = rangeE
        self._bioController.biometricReader.temperatureBase = rangeT    
    
    def restartEmotibit(self):
        if not self._gameIsReady:
            raise Exception("Game is not ready, please invoke setupGame() first") 
        elif not self._useEmotibit:
            return None
        self._bioController.restart()
    
    def updateAI(self, state):
        self._aiController.update(state)
    
    def getHeartRateRange(self):
        if not self._gameIsReady:
            raise Exception("Game is not ready, please invoke setupGame() first") 
        elif not self._useEmotibit:
            return None    
        return self._bioController.biometricReader.heartRateBase    
    
    def getEDARange(self):
        if not self._gameIsReady:
            raise Exception("Game is not ready, please invoke setupGame() first") 
        elif not self._useEmotibit:
            return None    
        return self._bioController.biometricReader.edaBase   

    def getTempRange(self):
        if not self._gameIsReady:
            raise Exception("Game is not ready, please invoke setupGame() first") 
        elif not self._useEmotibit:
            return None    
        return self._bioController.biometricReader.temperatureBase 

    def convertTTS(self, response):
        self._tts.generateTTS(response)

    def setUseEmotibit(self, useEmotibit):
        self._useEmotibit = useEmotibit

    def insertInteractionInDB(self):
        self._conversation.sendUserResponseToDB(self._sr.getStartTime(), self._sr.getEndTime(), self.userResponse, self.response)

    def resetConversation(self):
        self._conversation.resetConversation()



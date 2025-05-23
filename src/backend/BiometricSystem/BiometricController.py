from .BiometricReader import BiometricReader as br
import threading
from threading import Thread
# from GameStateSystem import GameState

class BiometricController:
    def __init__(self):
        self.nervous= False
        self._aiReference = None
        self.biometricReader= br()
        self.threadEvent = threading.Event()
        self.inputThread = Thread(target= self.read, daemon= True)
        self.inputThread.start()
        self._gameState = None
        self._gameIsReady = False
        self.emotibitErrorCount = 0
        self.errorFlag = False
        self.incrementError = False

        self.bcTestFlag = False
        
    def read(self):
        while self.threadEvent.is_set() == False:
            try:
                self.biometricReader.read()
                print("reading")
                #print("Error Count = 0")
                self.emotibitErrorCount = 0
                self.bcTestFlag = False
                self.isNervous(self.biometricReader.getHeartRate(), self.biometricReader.getTemperature(), self.biometricReader.getEDA())
                # print(type(self.biometricReader.getHeartRate()))
            except Exception as e:
                self.bcTestFlag = True

                if self.incrementError is True:
                    #print("Error Count +1")
                    self.emotibitErrorCount += 1

                if self.emotibitErrorCount > 3:
                    self.errorFlag = True 

                else:
                    self.reconnect(e)

    # From Matt
    # This method is called whenever the game state is updated in game state manager. 
    # So whenever the game stat is updated this class will now automatically, this class
    # has to know when the game state updates since the emotibit need to behave differently 
    # at certain states. When the game is in the initial phase is when we should be getting the baseline
    # and after that until the game finsihed is when the game should compare the hr to that basline as you already know.
    # Ill add some more functionality to this class so we can pass the isNervous data to the AI.  
    def update(self, state):
        self._gameState = state
        self.biometricReader.state = self._gameState.value

    def setAIReferece(self, ai):
        self._aiReference = ai

    def notifiyAIIfUserNervous(self):
        self._aiReference.updateNervous(self.isNervous)

    # The three methods above and the game state and ai reference in the constructor is what I have added

    def reconnect(self, error):
        #Will attempt to reconnect to emotibit so long as the game session has begun
        if self._gameIsReady == True:    
            print("Error - Attempting to reconnect to Emotibit")
            #self.biometricReader.clear()
            self.biometricReader.setup()
        
    def isNervous(self, heartRate, temperature, EDA):
        if heartRate > self.biometricReader.heartRateBase[1] or temperature > self.BiometricReader.temperatureBase[1] or EDA > self.biometricReader.edaBase[1]:
            self.setNervous(True)
        else:
            self.setNervous(False)
            
    def setNervous(self, isNervous):
        self.nervous= isNervous
        print(f"User Nervous: {self.nervous}")
        self.notifiyAIIfUserNervous()
        
    def getNervous(self):
        return self.nervous
    
    def getHeartRate(self):
        return self.biometricReader.getHeartRate()
    
    def getTemperature(self):
        return self.biometricReader.getTemperature()
    
    def getEDA(self):
        return self.biometricReader.getEDA()
    
    def clear(self):
        self.biometricReader.clear()

    def restart(self):
        self.biometricReader.restartBoard()

    def cleanThread(self):
        self.threadEvent.set()
        if self.inputThread is not None and self.inputThread.is_alive():
            print("Joining Biometric Thread")
            self.inputThread.join(timeout = 6)
    
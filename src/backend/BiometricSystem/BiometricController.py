from .BiometricReader import BiometricReader as br
from threading import Thread
from GameStateSystem.GameState import GameState

class BiometricController:
    def __init__(self):
        self.nervous= False
        self._aiReference = None
        self.biometricReader= br()
        self.inputThread = Thread(target= self.read, daemon= True)
        self.inputThread.start()
        self._gameState = None

    def read(self):
        while True:
            try:
                self.biometricReader.read()
                self.isNervous(self.biometricReader.getHeartRate())
                # print(type(self.biometricReader.getHeartRate()))
            except Exception as e:
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
        if self.gc.begin == True:    
            print("Error - Attempting to reconnect to Emotibit")
            #self.biometricReader.clear()
            self.biometricReader.setup()
        
    def isNervous(self, heartRate):
        if heartRate > 100.00:
            self.setNervous(True)
        else:
            self.setNervous(False)
            
    def setNervous(self, isNervous):
        self.nervous= isNervous
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
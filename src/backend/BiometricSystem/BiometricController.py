from BiometricSystem.BiometricReader import BiometricReader as br
from threading import Thread
from GameStateSystem import GameState


# The Biometric Controller should behave differently based on the game states. If the game is in the inital state it should
# read data and set the baselines
# afterwards it should just compare the heart rate to the basline
# TLDR some refactoring is needed to this class 


class BiometricController:
    def __init__(self):
        self.nervous= False
        self._aiReference = None
        self.biometricReader= br()
        self.inputThread = Thread(target= self.read, daemon= True)
        self.inputThread.start()

    def read(self):
        while True:
            try:
                self.biometricReader.read()
                self.isNervous(self.biometricReader.getHeartRate())
                # print(type(self.biometricReader.getHeartRate()))
            except Exception as e:
                self.reconnect(e)

                
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
        self.NotifyGC()
        
    def getNervous(self):
        return self.nervous
    
    def getHeartRate(self):
        return self.biometricReader.getHeartRate()
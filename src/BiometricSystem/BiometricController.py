from BiometricSystem.BiometricReader import BiometricReader as br
from threading import Thread

class BiometricController:
    def __init__(self, gameController, databaseController):
        self.nervous= False
        self.biometricReader= br()
        self.gc = gameController
        self.db= databaseController
        self.inputThread = Thread(target= self.read, daemon= True)
        self.inputThread.start()

    def read(self):
        while True:
            try:
                self.biometricReader.read()
                self.isNervous(self.biometricReader.getHeartRate())
                # print(type(self.biometricReader.getHeartRate()))
                self.sendToDB()
            except Exception as e:
                self.reconnect(e)
                
    def reconnect(self, error):
        print("Error - Attempting to reconnect to Emotibit")
        self.biometricReader.setup()

    def isNervous(self, heartRate):
        if heartRate > 80.00:
            self.setNervous(True)
        else:
            self.setNervous(False)
            
    def setNervous(self, isNervous):
        self.nervous= isNervous
        self.NotifyGC()

    def NotifyGC(self):
        self.gc.nervousUpdate()
        
    def getNervous(self):
        return self.nervous
    
    def sendToDB(self):
        self.db.insertBiometrics(self.biometricReader.getStartTime(), self.biometricReader.getEndTime(), self.biometricReader.getTemperature(), self.biometricReader.getHeartRate(), self.biometricReader.getEDA(), self.gc.session.getSessionID())
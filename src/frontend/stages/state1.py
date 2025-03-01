from backend.BackendInterface.GameManager import GameManager
from direct.task import Task
import numpy as np

class State1:
    def __init__(self):
        self.game = None
        self.state = None
        self.response = None
        self.endPhase = False

        self.heartRate = []
        self.temperature = []
        self.eda = []

        self.currentBaseH = 0
        self.currentBaseE = 0
        self.currentBaseT = 0

    def testPrint(self):
        print("This is state 1")

    def setGame(self, game):
        self.game = game
        taskMgr.doMethodLater(10, self.updateData, "data") 
    
    def begin(self):
        self.game._gameState.updateState(1)
        self.response = self.game.generateAIResponse()
        return self.response
        
    def convert(self):
        self.game.convertTTS(self.response)
    
    def generateResponse(self):
        self.response = self.game.generateAIResponse()

        if self.response == False:
            self.updateBaseValues()
            self.endPhase = True

        return self.response

    def updateData(self, task):
        self.heartRate.append(self.game.getUserHeartRate())
        self.eda.append(self.game.getUserEDA())
        self.temperature.append(self.game.getUserTemperature())

        if self.endPhase == False:
            return task.again
        else:
            return task.done

    def getAverageHeartRate(self):
        if len(self.heartRate) > 0:
            self.currentBaseH = self.doMath(self.heartRate)
            print(self.currentBaseH)
            return self.currentBaseH
        else:
            print("Error list length is 0.")
    
    def getAverageEDA(self):
        if len(self.eda) > 0:
            self.currentBaseE =  self.doMath(self.eda)
            return self.currentBaseE
        else:
            print("Error list legnth is 0.")

    def getAverageTemperature(self):
        if len(self.temperature) > 0:
            self.currentBaseT = self.doMath(self.temperature)
            return self.currentBaseT
        else:
            print("Error list length is 0")
    
    def doMath(self, data):
        data = [d for d in data if d is not None]
        mean = sum(data) / len(data)
        stdDiv = np.std(data, ddof = 1)

        lower = mean - (stdDiv + 5)
        upper = mean + (stdDiv + 5)

        return (lower, upper)
    
    def updateBaseValues(self):
        print(f"HR: {self.currentBaseH}")
        self.game.setRanges(self.currentBaseH, self.currentBaseE, self.currentBaseT)


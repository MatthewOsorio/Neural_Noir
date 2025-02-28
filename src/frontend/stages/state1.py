from backend.BackendInterface.GameManager import GameManager
from direct.task import Task
import numpy as np

class State1:
    def __init__(self):
        self.game = None
        self.state = None
        self.response = None

        self.heartRate = []
        self.temperature = []
        self.eda = []

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
        return self.response

    def updateData(self, task):
        self.heartRate.append(self.game.getUserHeartRate())
        self.eda.append(self.game.getUserEDA())
        self.temperature.append(self.game.getUserTemperature())
        return task.again

    def getAverageHeartRate(self):
        if len(self.heartRate) > 0:
            return self.doMath(self.heartRate)
        else:
            print("Error list length is 0.")
    
    def getAverageEDA(self):
        if len(self.eda) > 0:
            return self.doMath(self.eda)
        else:
            print("Error list legnth is 0.")

    def getAverageTemperature(self):
        if len(self.temperature) > 0:
            return self.doMath(self.temperature)
        else:
            print("Error list length is 0")
    
    def doMath(self, data):
        data = [d for d in data if d is not None]
        mean = sum(data) / len(data)
        stdDiv = np.std(data, ddof = 1)

        lower = mean - (stdDiv + 5)
        upper = mean + (stdDiv + 5)

        return (lower, upper)
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

        self.speakers = []
        self.texts = []
        self.audioFilePaths = []

    def testPrint(self):
        print("This is state 1")

    def setGame(self, game):
        self.game = game
        taskMgr.doMethodLater(5, self.updateData, "data") 
    
    def begin(self):
        self.game._gameState.updateState(1)
        self.response = self.game.generateAIResponse()
        return self.response
        
    def convert(self):
        self.game.convertTTS(self.response)
    
    def generateResponse(self):
        self.response = self.game.generateAIResponse()

        if self.response == False:
            self.getAverageHeartRate()
            self.getAverageEDA()
            self.getAverageTemperature()
            self.updateBaseValues()
            self.endPhase = True

        self.parseResponse(self.response)
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
            self.currentBaseH = self.doMath(self.heartRate, 0.8)
            print(self.currentBaseH)
            return self.currentBaseH
        else:
            print("Error list length is 0.")
    
    def getAverageEDA(self):
        if len(self.eda) > 0:
            self.currentBaseE =  self.doMath(self.eda, 0.1)
            return self.currentBaseE
        else:
            print("Error list legnth is 0.")

    def getAverageTemperature(self):
        if len(self.temperature) > 0:
            self.currentBaseT = self.doMath(self.temperature, 0.5)
            return self.currentBaseT
        else:
            print("Error list length is 0")
    
    def doMath(self, data, buffer):
        data = [d for d in data if d is not None]

        if len(data) > 0:
            mean = sum(data) / len(data)
            stdDiv = np.std(data, ddof = 1)

            lower = mean - (stdDiv + buffer)
            upper = mean + (stdDiv + buffer)

            return (lower, upper)
        
        else:
            return 0
    
    def updateBaseValues(self):
        #print(f"HR: {self.currentBaseH}")
        self.game.setRanges(self.currentBaseH, self.currentBaseE, self.currentBaseT)

    def cleanUpTasks(self):
        tskMgr.remove("data")

    def parseResponse(self, response):

        print (response)

        for line in response:
            self.speakers.append(line.get("Speaker"))
            self.texts.append(line.get("Text"))
            self.audioFilePaths.append(line.get("AudioFilepath"))
            print(f"audio path: {line.get('AudioFilepath')}")
    
    def resetResponse(self):
        self.speakers = []
        self.texts = []
        self.audioFilePaths = []


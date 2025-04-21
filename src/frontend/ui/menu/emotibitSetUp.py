from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectFrame, DirectButton, DGG
from panda3d.core import TextNode
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
import time
from direct.task import Task
from direct.interval.LerpInterval import LerpPosInterval
from backend.BiometricSystem.BiometricController import BiometricController

class EmotibitTutorial:
    def __init__(self, base):
        self.base = base
        self.active = False
        self.wordWrap = 50

        self.bc = None

        self.frame = DirectFrame(
            frameColor=(0, 0, 0, 1),
            frameSize=(-2, 2, -2, 2),
            parent=self.base.aspect2d
        )

        self.button = DirectButton(
            text="Back",
            scale=0.1,
            command=None,
            pos=(0, 0, -0.5),
            parent=self.frame
        )

        self.displayHeartRate = OnscreenText(
            text = "Heart Rate: 0",
            scale = 0.18,
            parent = self.frame,
            fg = (1,1,1,1),
            pos = (0,0.1,0)
        )

        self.displayEda = OnscreenText(
            text = "EDA: 0",
            scale = 0.18,
            parent = self.frame,
            fg = (1,1,1,1),
            pos = (0,-0.3,0)
        )

        self.displayTemperature = OnscreenText(
            text = "Temperature: 0",
            scale = 0.18,
            parent = self.frame,
            fg = (1,1,1,1),
            pos = (0,-0.7,0)
        )


        self.etTop = OnscreenText()
        self.et = OnscreenText()
        self.errorText = OnscreenText()

        self.warningTextCreator(self.etTop, "EmotiBit Set Up", (0, 0.9), 0.1, self.frame, (1, 1, 1, 1))
        self.warningTextCreator(
            self.et, 
            "Players who own an EmotiBit can use it to read their biometric data during gameplay. This game requires users connect to their EmotiBit via wifi connection." \
            "To connect your EmotiBit to your wifi, follow these steps:\n" 
            "          1. Remove the microSD card from the base of the EmotiBit.\n" 
            "          2. Insert the microSD card into your computer.\n" 
            "The box below will display the user's biometric data. If you have an EmotiBit connected, the values should update roughly every 5 seconds."
            "If there is no EmotiBit Connection, it will give an error message.", 
            (0, 0.5), 0.05, self.frame, (1, 1, 1, 1))
        self.warningTextCreator(
            self.errorText, 
            "Error: Cannot connect to EmotiBit.", 
            (0, 0.1), 0.05, self.frame, (1, 1, 1, 1))      

        self.hideAllBio()
        self.errorText.hide()  
        
    def show(self):
        self.active = True
        self.frame.show()
    
    def hide(self):
        self.active = False
        self.frame.hide()

    def warningTextCreator(self, item, text, pos, scale, parent, color):
        item = OnscreenText(
            text=text,
            pos=pos,
            scale=scale,
            parent=parent,
            fg=color,
            wordwrap= self.wordWrap
        )

    def updateBiometric(self, task):
        print("Update BC task")
        heartRate = self.getHeartRate()  
        if heartRate is not None and self.bc.bcTestFlag is not True:
            self.showAllBio()
            print("HR data")
            self.displayHeartRate.setText("Heart Rate: " + str(round(heartRate, 2)))
            
        eda = self.getEda()
        if eda is not None and self.bc.bcTestFlag is not True:
            self.displayEda.setText("EDA: " + str(round(eda, 2)))
            
        temperature = self.getTemperature()
        if temperature is not None and self.bc.bcTestFlag is not True:
            self.displayTemperature.setText("Temperature: " + str(round(temperature, 2)))

        if self.bc.bcTestFlag is True:
            self.hideAllBio()
            print("No data")
            
        return task.again
        
    def showAllBio(self):
        self.displayHeartRate.show()
        self.displayTemperature.show()
        self.displayEda.show()
        self.errorText.hide()

    def hideAllBio(self):
        self.displayHeartRate.hide()
        self.displayTemperature.hide()
        self.displayEda.hide()
        self.errorText.show()

    def getHeartRate(self):
        hr = self.bc.getHeartRate()
        return hr
    
    def getEda(self):
        eda = self.bc.getEDA()
        return eda
    
    def getTemperature(self):
        temp = self.bc.getTemperature()
        return temp
    
    def show(self):
        self.frame.show()
    
    def hide(self):
        self.frame.hide()
    
    def cleanUp(self):
        self.bc._gameIsReady = False
        self.bc.cleanThread()
        taskMgr.remove("updateBio")
        self.bc = None

    def goBack(self):
        self.cleanUp()
        self.hide()
        self.displayHeartRate.setText("Heart Rate: " + str(0))
        self.displayEda.setText("EDA: " + str(0))
        self.displayTemperature.setText("Temperature: " + str(0))

    def setUpBC(self):
        self.bc = BiometricController()
        self.bc._gameIsReady = True
        print("Starting bc task")
        taskMgr.doMethodLater(5, self.updateBiometric, "updateBio") 
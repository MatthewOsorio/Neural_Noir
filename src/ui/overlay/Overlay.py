from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectFrame, DirectButton, DGG
from panda3d.core import TextNode
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
import time
from direct.task import Task
from panda3d.core import TransparencyAttrib


class Overlay:
    def __init__(self, base):
        self.base = base
        self.overlay = DirectFrame(
            frameColor=(0, 0, 0, 0),
            frameSize=(-1, 1, -1, 1),
            parent=self.base.base.aspect2d
        )
        self.overlay.hide()

        self.bioBackground = OnscreenImage(
            self.base.base.menuManager.backGroundBlack,
            parent=self.overlay,
            scale=(0.3, 0.3, 0.3),
            pos=(-1.5 , 0, -0.6),
        )

        self.bioBackground.setColor(0, 0, 0, 0.5)
        self.bioBackground.setTransparency(TransparencyAttrib.MAlpha)

        self.displayHeartRate = OnscreenText(
            text = "Heart Rate: 0",
            font = loader.loadFont("../Assets/Fonts/Limelight/Limelight-Regular.ttf"),
            scale = 0.18,
            parent = self.bioBackground,
            fg = (1,1,1,1),
            pos = (0,0.1,0)
        )

        self.displayEda = OnscreenText(
            text = "EDA: 0",
            font = loader.loadFont("../Assets/Fonts/Limelight/Limelight-Regular.ttf"),
            scale = 0.18,
            parent = self.bioBackground,
            fg = (1,1,1,1),
            pos = (0,-0.3,0)
        )

        self.displayTemperature = OnscreenText(
            text = "Temperature: 0",
            font = loader.loadFont("../Assets/Fonts/Limelight/Limelight-Regular.ttf"),
            scale = 0.18,
            parent = self.bioBackground,
            fg = (1,1,1,1),
            pos = (0,-0.7,0)
        )

        self.PTTButton = DirectButton(
            text = "PTT",
            scale = 0.15,
            pos = (1.5, 0, -0.7),
            parent = self.overlay,
            command = None,
            image = "../Assets/Images/button.png",
            frameColor=(0, 0, 0, 0)
        )

        self.PTTButton.setTransparency(TransparencyAttrib.MAlpha)

        self.subtitles = OnscreenText(
            text = "Subtitles",
            font = loader.loadFont("../Assets/Fonts/Limelight/Limelight-Regular.ttf"),
            scale = 0.15,
            parent = self.overlay,
            fg = (1,1,1,1),
            pos = (0,0,0)
        )
        
        taskMgr.doMethodLater(10, self.updateOverlay, "updateOverlayTask") 
    
    def show(self):
        self.overlay.show()
    
    def hide(self):
        self.overlay.hide()
    
    def getHeartRate(self):
        self.heartRate = self.base.game.biometricController.biometricReader.heartRate
        return self.heartRate
    
    def getEda(self):
        self.eda = self.base.game.biometricController.biometricReader.eda
        return self.eda
    
    def getTemperature(self):
        self.temperature = self.base.game.biometricController.biometricReader.temperature
        return self.temperature
    
    def updateOverlay(self, task):  
        self.heartRate = self.getHeartRate()  
        if self.heartRate is not None:
            self.displayHeartRate.setText("Heart Rate: " + str(round(self.heartRate, 2)))
        if self.heartRate is None:
            self.displayHeartRate.setText("Heart Rate: 0")

        self.eda = self.getEda()
        if self.eda is not None:
            self.displayEda.setText("EDA: " + str(round(self.eda, 2)))
        if self.eda is None:
            self.displayEda.setText("EDA: 0")

        self.temperature = self.getTemperature()
        if self.temperature is not None:
            self.displayTemperature.setText("Temperature: " + str(round(self.temperature, 2)))
        if self.temperature is None:
            self.displayTemperature.setText("Temperature: 0")

        return task.again
    
    
    def showPTTButton(self):
        self.PTTButton.show()
    
    def hidePTTButton(self):   
        self.PTTButton.hide()

    #Updates the subtitles to the response from the detective 
    #Will be moved into its own class
    def updateSubtitles(self, text):
        self.subtitles.setText(text)
    
    def showSubtitles(self):
        self.subtitles.show()

    def hideSubtitles(self):
        self.subtitles.hide()
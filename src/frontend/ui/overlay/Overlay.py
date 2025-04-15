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
from ..overlay.flashback import flashback
from ..overlay.PTT import PTT
from ..overlay.subtitles import Subtitles
from ..overlay.error import ErrorScreen
from ..overlay.userSpeech import UserSpeech
from ..overlay.tutorials import Tutorial
import threading

class Overlay:
    def __init__(self, base):
        self.base = base

        self.threadEvent = threading.Event()
        self.internetThread = None

        self.flashback = flashback(self.base)

        self.ptt = PTT(self.base)
        self.subtitles = Subtitles(self.base)
        self.userSpeech = UserSpeech(self.base)

        self.errorScreen = ErrorScreen(self.base)
        self.tutorials = Tutorial(self.base)

        self.connectionError = False
        self.initialImageFinished = False

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

        self.bioBackground.setColor(0, 0, 0, 0.7)
        self.bioBackground.setTransparency(TransparencyAttrib.MAlpha)

        self.bioTitle = OnscreenText(
            text = "Biometrics",
            font = loader.loadFont("../Assets/Fonts/Limelight/Limelight-Regular.ttf"),
            scale = 0.25,
            parent = self.bioBackground,
            fg = (1,1,1,1),
            pos = (0,0.6,0)            
        )

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

        self.acceptSpeechButton = DirectButton(
            text = "ACCEPT",
            scale = 0.1,
            pos = (1.5, 0, -0.5),
            command = None,
            parent = self.overlay,
            frameColor=(0, 0, 0, 1),
            text_fg = (1, 1, 1, 1),
            sortOrder=1
        )

        self.redoSpeechButton = DirectButton(
            text = "RETAKE",
            scale = 0.1,
            pos = (1.5, -0.1, -0.7),
            command = None,
            parent = self.overlay,
            frameColor=(0, 0, 0, 1),
            text_fg = (1, 1, 1, 1),
            sortOrder=1
        )

        self.subtitlesBox = OnscreenImage(
            self.base.base.menuManager.backGroundBlack,
            parent=self.overlay,
            scale=(1, 0.3, 0.3),
            pos=(0 , 0, -0.6),
        ) 

        self.userInputBox = OnscreenImage(
            self.base.base.menuManager.backGroundBlack,
            parent=self.overlay,
            scale=(1, 0.3, 0.3),
            pos=(0 , 0, -0.6),
        )              
        
        self.subtitlesBox.setColor(0, 0, 0, 0.7)
        self.subtitlesBox.setTransparency(TransparencyAttrib.MAlpha)

        self.subtitles.setParent(self.subtitlesBox)
        self.subtitlesBox.hide()

        self.userInputBox.setColor(0, 0, 0, 0.7)
        self.userInputBox.setTransparency(TransparencyAttrib.MAlpha)
        self.userSpeech.setParent(self.userInputBox)
        self.userInputBox.hide()

        self.ptt.setButton(self.PTTButton)
        self.ptt.hidePTTButton()
        self.setButtonCommand()
        
        self.hideBioData()

        self.errorScreen.hideConnectionError()
       # self.errorScreen.hideOpenAIError()

        self.hideUserInputBox()
        self.setAcceptButtonCommand()
        self.setRedoButtonCommand()

        taskMgr.doMethodLater(5, self.updateOverlay, "updateOverlayTask") 
        taskMgr.doMethodLater(5, self.checkInternetConnection, "checkConnectionTask") 


    def show(self):
        self.overlay.show()
    
    def hide(self):
        self.overlay.hide()
    
    def getHeartRate(self):
        self.heartRate = self.base.game.getUserHeartRate()
        return self.heartRate
    
    def getEda(self):
        self.eda = self.base.game.getUserEDA()
        return self.eda
    
    def getTemperature(self):
        self.temperature = self.base.game.getUserTemperature()
        return self.temperature
    
    def updateOverlay(self, task):  
        self.heartRate = self.getHeartRate()  
        if self.heartRate is not None:
            self.displayHeartRate.setText("Heart Rate: " + str(round(self.heartRate, 2)))
            if self.base.current > 0:
                if self.heartRate > self.base.game.getHeartRateRange()[1]:
                    self.displayHeartRate.setFg((1, 0, 0, 1))
                else:
                    self.displayHeartRate.setFg((1, 1, 1, 1))
        if self.heartRate is None:
            self.displayHeartRate.setText("Heart Rate: 0")

        self.eda = self.getEda()
        if self.eda is not None:
            self.displayEda.setText("EDA: " + str(round(self.eda, 2)))
            if self.base.current > 0:
                if self.eda > self.base.game.getEDARange()[1]:
                    self.displayEda.setFg((1, 0, 0, 1))
                else:
                    self.displayEda.setFg((1, 1, 1, 1))
        if self.eda is None:
            self.displayEda.setText("EDA: 0")

        self.temperature = self.getTemperature()
        if self.temperature is not None:
            self.displayTemperature.setText("Temperature: " + str(round(self.temperature, 2)))
            if self.base.current > 0:
                if self.temperature > self.base.game.getTempRange()[1]:
                    self.displayTemperature.setFg((1, 0, 0, 1))
                else:
                    self.displayTemperature.setFg((1, 1, 1, 1))
        if self.temperature is None:
            self.displayTemperature.setText("Temperature: 0")

        return task.again
    
    
    def showSubtitlesBox(self):
        self.subtitlesBox.show()

    def hideSubtitlesBox(self):
        self.subtitlesBox.hide()

    def showUserInputBox(self):
        self.userInputBox.show()
        self.acceptSpeechButton.show()
        self.redoSpeechButton.show()
        #self.userSpeech.active = True
    
    def hideUserInputBox(self):
        self.userInputBox.hide()
        self.acceptSpeechButton.hide()
        self.redoSpeechButton.hide()

    def setButtonCommand(self):
        self.PTTButton["command"] = self.ptt.setInactive

    def setAcceptButtonCommand(self):
        self.acceptSpeechButton["command"] = self.userSpeech.setInactive
    
    def setRedoButtonCommand(self):
        self.redoSpeechButton["command"] = self.userSpeech.setInactiveSignalRedo

    def hideBioData(self):
        self.bioBackground.hide()
    
    def showBioData(self):
        self.bioBackground.show()

    def hideAll(self):
        self.bioBackground.hide()
        self.subtitlesBox.hide()
        self.userInputBox.hide()
        self.PTTButton.hide()
        self.PTTButton.noError = False
        self.acceptSpeechButton.hide()
        self.redoSpeechButton.hide()
        self.flashback.hide()
        self.base.menu.pauseMenu.hide()

    def checkInternetConnection(self, task):
        self.internetThread = threading.Thread(target=self.checkInternetThread, daemon=True)
        self.internetThread.start()
        return task.again

    def checkInternetThread(self):
        #print("check (background thread)")
        self.connection = self.base.base.connection
        status = self.connection.checkInternet()

        if not status and not self.connectionError:
            self.connectionError = True

            # Show error on the main thread
            taskMgr.add(lambda task: self.handleConnectionError(task), "showConnectionErrorTask")

    #check connection to OpenAI API if there is internet 
    def checkGPTConnection(self):
        status = self.connection.checkOpenai()

        if not status and not self.connectionError:
            self.connectionError = True
            
            taskMgr.add(lambda task: self.handleOpenAIError(task), "showConnectionErrorTask")
        
    def handleConnectionError(self, task):
        self.hideAll()
        self.base.pausable = False
        self.errorScreen.showConnectionError()
        return task.done  

    def handleOpenAIError(self, task):
        self.hideAll()
        self.base.pausable = False
        self.errorScreen.connectionErrorText.setText("OpenAI Error")
        self.errorScreen.connectionErrorText2.setText("Please check your OpenAI API key.")
        self.errorScreen.showConnectionError()
        return task.done  
    
    #NOTE This will automatically end the game if the emotibit connection is lost for around 15 seconds while emotibit mode is on
    #If for some reason you need to test something with emotibit mode on, disable "self.Overlay.startEmotiBitCheck()" in beginInterrogation function in interrogationRoom
    def startEmotiBitCheck(self):
        if self.base.useEmotibit is True:
            taskMgr.doMethodLater(5, self.checkEmotiBitConnection, "checkEmotiBitConnectionTask")

    def checkEmotiBitConnection(self, task):
        status = self.base.game._bioController.errorFlag
        #print(f"Emotibit Error Count: {self.base.game._bioController.emotibitErrorCount}")
        if status and not self.connectionError:
            self.connectionError = True
            
            # Show error on the main thread
            taskMgr.add(lambda task: self.handleEmotiBitError(task), "showConnectionErrorTask")

        return task.again

    def handleEmotiBitError(self, task):
        self.hideAll()
        self.base.pausable = False
        self.errorScreen.connectionErrorText.setText("EmotiBit Error")
        self.errorScreen.connectionErrorText2.setText("Please check your EmotiBit connection.")
        self.errorScreen.showConnectionError()
        return task.done


    def cleanUpTasks(self):
        taskMgr.remove("updateOverlayTask")
        taskMgr.remove("checkConnectionTask")
        taskMgr.remove("showConnectionErrorTask")
        if self.base.useEmotibit is True:
            taskMgr.remove("checkEmotiBitConnectionTask")

    def cleanUpThreads(self):
        self.threadEvent.set()
        print("Internt thread clean up function")
        if self.internetThread is not None:
            print("Joining internet check thread")
            self.internetThread.join()
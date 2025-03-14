from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectFrame, DirectButton, DGG
from panda3d.core import TextNode
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
import time 
import sys

from ui.audio import audioManager
import ui.ScriptDisplay as ScriptDisplay


#Controls menu navigation and allows each menu to use Aspect2d from main
#In menu classes, use manager.base.aspect2D to use Aspect2d 
class menuManager:
    def __init__(self, base, startFlag):
        self.base = base
        self.titleImage = None
        self.initializeBackground()
        
        self.audio = audioManager(self.base)
        
        #Instance of each menu
        self.mainMenu = mainMenu(self)
        self.settingsMenu = settingsMenu(self)
        self.audioMenu = audioSettings(self)
        self.quitMenu = confirmQuit(self)

        self.titleImage = OnscreenImage(
            image='../images/Room_Backdrop_Blur.png', 
            parent=self.base.render2d,
            sort=1
        )
        self.titleImage.setName("MainMenuBackground") # assign a name to the image to debug nodes

        self.gameStart = startFlag
        self.gameState = 'menu'

    def initializeBackground(self):
        if self.titleImage is not None: 
            self.titleImage.hide() # hide the background if the game has started
        self.titleImage = OnscreenImage(
            image='../images/Room_Backdrop_Blur.png',
            parent=self.base.render2d
        )
        self.showImage()
        
    def showMain(self):
        self.mainMenu.show()
        self.gameState = 'menu'

    def showSettings(self):
        self.settingsMenu.show()
        self.gameState = 'menu'

    def showAudio(self):
        self.audioMenu.show()

    def showQuit(self):
        self.quitMenu.show()

    def hideImage(self):
        self.titleImage.hide()

    def showImage(self):
        self.titleImage.show()

    def beginGame(self):
        self.gameStart = True
        #print("Menu -", self.gameStart)
        self.gameState = 'gameplay'
        
#The Main menu screen. 
class mainMenu:
    def __init__(self, manager):

        self.manager = manager

        self.mainMenu = DirectFrame(
            frameColor=(0, 0, 0, 0),
            frameSize=(-1, 1, -1, 1),
            parent=self.manager.base.aspect2d
        )

        self.titleText = TextNode('TitleText')
        self.titleText.setText("Neural Noir")
        self.titleText_np = self.mainMenu.attachNewNode(self.titleText)  
        self.titleText_np.setScale(0.3)
        self.titleText_np.setPos(0, 0, 0.7)
        self.titleText.setAlign(self.titleText.ACenter)

        self.startButton = DirectButton(
            text="Start Game",
            scale=0.1,
            pos=(0, 0, 0.3),
            parent=self.mainMenu,
            command = self.startGame
        )
 
        self.settingsButton = DirectButton(
            text="Settings",
            scale=0.1,
            pos=(0, 0, 0.0),
            parent=self.mainMenu,
            command=self.moveToSettings
        )

        self.quitButton = DirectButton(
            text="Quit",
            scale=0.1,
            pos=(0, 0, -0.3),
            parent=self.mainMenu,
            command=self.moveToQuit
        )

        self.bottomText = TextNode('BottomText')
        self.bottomText.setText("Created by CS425 T25")
        self.bottomText_np = self.mainMenu.attachNewNode(self.bottomText)  
        self.bottomText_np.setScale(0.07)
        self.bottomText_np.setPos(0, 0, -0.9)
        self.bottomText.setAlign(self.bottomText.ACenter)

    def startGame(self):
        self.hide()
        self.manager.hideImage()
        self.manager.beginGame()

    def moveToSettings(self):
        self.hide()
        self.manager.showSettings()     

    def moveToQuit(self):
        self.hide()
        self.manager.showQuit()
        

    def show(self):
        self.mainMenu.show()

    def hide(self):
        self.mainMenu.hide()


class settingsMenu:
    def __init__(self, manager):
        self.manager = manager

        self.settingsMenu = DirectFrame(
            frameColor=(0, 0, 0, 0),
            frameSize=(-1, 1, -1, 1),
            parent=self.manager.base.aspect2d
        )
        self.hide()

        self.topText = TextNode('TopText')
        self.topText.setText("Settings")
        self.topText_np = self.settingsMenu.attachNewNode(self.topText)  
        self.topText_np.setScale(0.25)
        self.topText_np.setPos(0, 0, 0.7)
        self.topText.setAlign(self.topText.ACenter)

        self.backButton = DirectButton(
            text="Back",
            scale=0.1,
            pos=(0, 0, 0),
            parent=self.settingsMenu,
            command=self.moveToMain
        )

        self.audioButton = DirectButton(
            text="Audio",
            scale=0.1,
            pos=(0, 0, 0.3),
            command=self.moveToAudio,
            parent=self.settingsMenu
        )

    def moveToMain(self):
        self.hide()
        self.manager.showMain()

    def moveToAudio(self):
        self.hide()
        self.manager.showAudio()

    def show(self):
        self.settingsMenu.show()
        
    def hide(self):
        self.settingsMenu.hide()
        

class audioSettings:
    def __init__(self, manager, back_callback=None):    

        self.manager = manager
        self.back_callback = back_callback

        self.audioMenu = DirectFrame(
            frameColor=(0, 0, 0, 0), 
            frameSize=(-1, 1, -1, 1), 
            parent=self.manager.base.aspect2d
        )

        self.topText = TextNode('TopText')
        self.topText.setText("Audio Settings")
        self.topText_np = self.audioMenu.attachNewNode(self.topText)
        self.topText_np.setScale(0.2)
        self.topText_np.setPos(0, 0, 0.8)
        self.topText.setWordwrap(25.0)
        self.topText.setAlign(self.topText.ACenter)

        self.volumeText = OnscreenText(
            text = 'Sfx Volume',
            scale = 0.15,
            parent = self.audioMenu,
            fg = (1,1,1,1),
            pos = (0,0.5,0.5)
        )

        self.volumeSlider = DirectSlider(
            range=(0,1),
            pageSize = 20,
            pos=(0, 0.4, 0.4),
            scale=0.5,
            parent = self.audioMenu,
            value=0.5,
            command=self.setVolumeV
        )

        self.voiceVolumeText = OnscreenText(
            text = 'Dialogue Volume',
            scale = 0.15,
            parent = self.audioMenu,
            fg = (1,1,1,1),
            pos = (0,0.2,0.2)
        )

        self.voiceVolumeSlider = DirectSlider(
            range=(0,1),
            pageSize = 20,
            pos=(0, 0.1, 0.1),
            scale=0.5,
            parent = self.audioMenu,
            value=0.5,
            command=self.setVoiceVolumeV
        )

        self.subTitlesText = OnscreenText(
            text = 'Subtitles',
            scale = 0.15,
            parent = self.audioMenu,
            fg = (1,1,1,1),
            pos = (0, -0.2 ,-0.3)
        )

        self.subTitlesOn = DirectCheckButton(
            text = "On",
            parent = self.audioMenu,
            scale = 0.1,
            pos = (-0.3, -0.3, -0.4),
            command = self.turnSubtitlesOn
        )

        self.subTitlesOff = DirectCheckButton(
            text = "Off",
            parent = self.audioMenu,
            scale = 0.1,
            pos = (0.4, -0.3, -0.4),
            command = self.turnSubtitlesOff
        )

        self.backButton = DirectButton(
            text = ("Back"),
            scale = 0.12,
            pos = (0,0,-0.7),
            parent = self.audioMenu,
            command = self.handleBack
        )

        self.testInput = DirectButton(
            text = ("Test Microphone"),
            scale = 0.1,
            pos = (-0.4,0,-0.9),
            parent = self.audioMenu,
            command = self.manager.audio.testAudioInput
        )

        self.testOutput = DirectButton(
            text = ("Test Speakers"),
            scale = 0.1,
            pos = (0.4,0,-0.9),
            parent = self.audioMenu,
            command = self.manager.audio.testAudioOutput
        )

        self.hide()

    def handleBack(self):
        if self.back_callback:
            self.hide()
            self.back_callback()
        else:
            self.hide()
            self.moveToSettings()

    def moveToSettings(self):
        self.hide()
        self.manager.showSettings()

    def show(self):
        self.audioMenu.show()

    def hide(self):
        self.audioMenu.hide()

    def setVolumeV(self):
        self.manager.audio.setVolumeValue(self.volumeSlider['value'])

    def setVoiceVolumeV(self):
        if self.manager.gameStart == True:
            self.manager.base.interrogationRoom.game.tts.audio.setVolume(self.voiceVolumeSlider['value'])

    def turnSubtitlesOn(self, state):
        self.subTitlesOff["indicatorValue"] = False
        self.subTitlesOff.setIndicatorValue
    
    def turnSubtitlesOff(self, state):
        self.subTitlesOn["indicatorValue"] = False
        self.subTitlesOn.setIndicatorValue

#ConfirmQuit code originally written by Matt
#Modified and integrated by Evie 
class confirmQuit:

    def __init__(self, manager):
        self.manager = manager

        self.createContents()
        self.hide()

    def createContents(self):
        self.parentFrame = DirectFrame(frameColor=(0, 0, 0, 0),
                            frameSize=(-0.75, 0.75, -0.75, 0.75),
                            pos= (0, 0, 0),
                            parent=self.manager.base.aspect2d)
        
        titleText= 'Are you sure?'
        #TitleFrame= DirectFrame(parent= parentFrame,
                                #frameColor= (0, 0, 0, 0),
                                #frameSize= (-0.50, 0.50, -0.25, 0.25),
                                #pos= (0, 0, 0.5))
        
        self.titleTextFrame= DirectLabel(parent= self.parentFrame,
                                    text= titleText,
                                    text_scale= (0.1, 0.1),
                                    text_fg= (255, 255, 255, 0.9),
                                    frameColor= (0, 0, 0, 0),
                                    pos = (0,0.5,0.5))
        
        self.yesButtom= DirectButton(parent= self.parentFrame,
                                text="Yes",
                                scale= 0.075,
                                pos= (-0.40, 0, 0),
                                command = sys.exit)
        
        self.noButtom= DirectButton(parent= self.parentFrame,
                        text="No",
                        scale= 0.075,
                        pos= (0.40, 0, 0),
                        command = self.moveToMain)
        
    def moveToMain(self):
        self.hide()
        self.manager.showMain()

    def hide(self):
        self.parentFrame.hide()

    def show(self):
        self.parentFrame.show()
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectFrame, DirectButton, DGG
from panda3d.core import TextNode
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
import sys

from ui.menu.MainMenu import mainMenu
from ui.menu.SettingsMenu import settingsMenu
from ui.menu.AudioMenu import audioSettings
from ui.menu.PauseMenu import PauseMenu

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
        
        self.gameStart = startFlag
        self.gameState = 'menu'

        self.limeLight = "../Assets/Fonts/Limelight/Limelight-Regular.ttf"
        self.mainBackGround = "../Assets/Images/NeuralNoir_Background_Image.jpg"
        self.backGroundBlack = "../Assets/Images/Black.jpg"
        
        #Instance of each menu
        self.mainMenu = mainMenu(self, self.base)
        self.settingsMenu = settingsMenu(self, self.base)
        self.audioMenu = audioSettings(self, self.base, self.audio)
        self.pauseMenu = None
        self.quitMenu = confirmQuit(self)

        self.subtitles = False

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

    def initializePauseMenu(self):
        self.pauseMenu = PauseMenu(self, self.base)
        

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
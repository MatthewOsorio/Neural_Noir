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
from ui.menu.QuitMenu import confirmQuit

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
        self.quitMenu = confirmQuit(self, self.base)

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
        self.quitMenu.showParent()

    def hideImage(self):
        self.titleImage.hide()

    def showImage(self):
        self.titleImage.show()
    
    def showQuitPause(self):
        self.pauseMenu.hide()
        self.quitMenu.showFromPause()

    def beginGame(self):
        self.gameStart = True
        #print("Menu -", self.gameStart)
        self.gameState = 'gameplay'

    def initializePauseMenu(self):
        self.pauseMenu = PauseMenu(self, self.base)
    
    def showPauseHideQuit(self):
        self.quitMenu.hide()
        self.pauseMenu.displayPauseMenu()
    
        
        

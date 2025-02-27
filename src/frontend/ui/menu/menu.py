from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectFrame, DirectButton, DGG
from panda3d.core import TextNode
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
import sys

from frontend.ui.menu.MainMenu import mainMenu
from frontend.ui.menu.SettingsMenu import settingsMenu
from frontend.ui.menu.AudioMenu import audioSettings
from frontend.ui.menu.PauseMenu import PauseMenu
from frontend.ui.menu.QuitMenu import confirmQuit

from frontend.ui.audio import audioManager
import frontend.ui.ScriptDisplay as ScriptDisplay

import os
from panda3d.core import Filename
current_dir = os.path.dirname(os.path.abspath(__file__))
Background = os.path.join(current_dir, "..", "..", "..", "..", "Assets", "Images", "NeuralNoir_Background_Image.jpg")
Background = os.path.normpath(Background)
Background = Filename.fromOsSpecific(Background).getFullpath()

Black = os.path.join(current_dir, "..", "..", "..", "..", "Assets", "Images", "Black.jpg")
Black = os.path.normpath(Black)
Black = Filename.fromOsSpecific(Black).getFullpath()

Room = os.path.join(current_dir, "..", "..", "..", "..", "Assets", "Images", "Room_Backdrop_Blur.png")
Room = os.path.normpath(Room)
Room = Filename.fromOsSpecific(Room).getFullpath()

Limelight = os.path.join(current_dir, "..", "..", "..", "..", "Assets", "Fonts", "Limelight", "Limelight-Regular.ttf")
Limelight = os.path.normpath(Limelight)
Limelight = Filename.fromOsSpecific(Limelight).getFullpath()

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

        self.mainBackground = base.loader.loadTexture(Background)
        self.black = base.loader.loadTexture(Black)
        self.room = base.loader.loadTexture(Room)
        self.font = base.loader.loadFont(Limelight)

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
    
        
        

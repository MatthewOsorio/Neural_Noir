from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectFrame, DirectButton, DGG
from panda3d.core import TextNode
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import *
from direct.gui.OnscreenText import OnscreenText
import time 

class menuManager:
    def __init__(self, base):
        self.base = base

        self.mainMenu = mainMenu(self)
        self.settingsMenu = settingsMenu(self)

    def showMain(self):
        self.mainMenu.show()
        self.settingsMenu.hide()

    def showSettings(self):
        self.settingsMenu.show()
        self.mainMenu.hide()


class mainMenu:
    def __init__(self, manager):
        self.manager = manager

        self.mainMenu = DirectFrame(
            frameColor=(0, 0, 0, 1),
            frameSize=(-1, 1, -1, 1),
            parent=self.manager.base.aspect2d
        )

        self.titleImage = OnscreenImage(
            image='Room_backdrop.png', 
            parent=self.mainMenu
        )
      
        self.titleText = TextNode('TitleText')
        self.titleText.setText("Title")
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
            parent=self.mainMenu
        )

        self.bottomText = TextNode('BottomText')
        self.bottomText.setText("Created by CS425 T25")
        self.bottomText_np = self.mainMenu.attachNewNode(self.bottomText)  
        self.bottomText_np.setScale(0.07)
        self.bottomText_np.setPos(0, 0, -0.9)
        self.bottomText.setAlign(self.bottomText.ACenter)

    def startGame(self):
        self.hide()

    def moveToSettings(self):
        self.hide()
        self.manager.showSettings()     

    def show(self):
        self.mainMenu.show()

    def hide(self):
        self.mainMenu.hide()


class settingsMenu:
    def __init__(self, manager):
        self.manager = manager

        self.settingsMenu = DirectFrame(
            frameColor=(0, 0, 0, 1),
            frameSize=(-1, 1, -1, 1),
            parent=self.manager.base.aspect2d
        )

        self.titleImage = OnscreenImage(
            image='Room_backdrop.png', 
            parent=self.settingsMenu
        )

        self.topText = TextNode('TopText')
        self.topText.setText("Settings")
        self.topText_np = self.settingsMenu.attachNewNode(self.topText)
        self.topText_np.setScale(0.2)
        self.topText_np.setPos(-0.2, 0, 0.7)

        self.backButton = DirectButton(
            text="Back",
            scale=0.1,
            pos=(0, 0, 0),
            parent=self.settingsMenu,
            command=self.manager.showMain
        )

    def show(self):
        self.settingsMenu.show()

    def hide(self):
        self.settingsMenu.hide()
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectFrame, DirectButton, DGG
from panda3d.core import TextNode
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *

class mainMenu:
    def __init__(self, manager, base):

        self.base = base
        self.manager = manager

        self.mainMenu = DirectFrame(
            frameColor=(0, 0, 0, 0),
            frameSize=(-1, 1, -1, 1),
            parent=self.base.aspect2d
        )

        self.backdrop = OnscreenImage(
            self.manager.mainBackground,
            pos = (1, 0, 0), 
            parent = self.mainMenu)
        
        self.backdropBack = OnscreenImage(
            self.manager.black,
            pos = (-1, 0, 0),
            parent = self.mainMenu
        )

        self.titleText = TextNode('TitleText')
        self.titleText.setText("Neural Noir")
        self.titleText_np = self.mainMenu.attachNewNode(self.titleText)  
        self.titleText_np.setScale(0.25)
        self.titleText_np.setPos(-1, 0, 0.7)
        self.titleText.setAlign(self.titleText.ACenter)
        self.titleText.font = self.manager.font
        self.mainTextColor = (1,1,1,1)
        self.hoverColor = (1,1,0.5,1)

        self.startButton = DirectButton(
            text="Start Game",
            text_font = self.manager.font,
            scale=0.1,
            pos=(-1, 0, 0.3),
            parent=self.mainMenu,
            command = self.startGame,
            frameColor = (0,0,0,0),
            text_fg=self.mainTextColor,
        )
 
        self.settingsButton = DirectButton(
            text="Settings",
            text_font = self.manager.font,
            text_fg = (1,1,1,1),
            scale=0.1,
            pos=(-1, 0, 0.0),
            parent=self.mainMenu,
            command=self.moveToSettings,
            frameColor = (0,0,0,0)
        )

        self.quitButton = DirectButton(
            text="Quit",
            text_font = self.manager.font,
            text_fg = (1,1,1,1),
            scale=0.1,
            pos=(-1, 0, -0.3),
            parent=self.mainMenu,
            command=self.moveToQuit,
            frameColor = (0,0,0,0)
        )

        self.bottomText = TextNode('BottomText')
        self.bottomText.setText("Created by CS425 T25")
        self.bottomText_np = self.mainMenu.attachNewNode(self.bottomText)  
        self.bottomText_np.setScale(0.07)
        self.bottomText_np.setPos(-1, 0, -0.9)
        self.bottomText.setAlign(self.bottomText.ACenter)
        self.bottomText.font = self.manager.font

        self.startButton.bind(DGG.ENTER, lambda event: self.setColorHover(self.startButton))  # Mouse enters
        self.startButton.bind(DGG.EXIT, lambda event: self.setColorDefault(self.startButton)) 

        self.settingsButton.bind(DGG.ENTER, lambda event: self.setColorHover(self.settingsButton))  # Mouse enters
        self.settingsButton.bind(DGG.EXIT, lambda event: self.setColorDefault(self.settingsButton)) 

        self.startButton.bind(DGG.ENTER, lambda event: self.setColorHover(self.startButton))  # Mouse enters
        self.startButton.bind(DGG.EXIT, lambda event: self.setColorDefault(self.startButton)) 

        self.quitButton.bind(DGG.ENTER, lambda event: self.setColorHover(self.quitButton))  # Mouse enters
        self.quitButton.bind(DGG.EXIT, lambda event: self.setColorDefault(self.quitButton)) 
        

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

    def setColorHover (self, button):
        button["text_fg"] = self.hoverColor

    def setColorDefault (self, button):
        button["text_fg"] = self.mainTextColor

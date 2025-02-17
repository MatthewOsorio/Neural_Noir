from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectFrame, DirectButton, DGG
from panda3d.core import TextNode
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *

limeLight = "../Assets/Fonts/Limelight/Limelight-Regular.ttf"

class settingsMenu:
    def __init__(self, manager, base):
        self.base = base
        self.manager = manager

        self.mainTextColor = (1,1,1,1)
        self.hoverColor = (1,1,0.5,1)

        self.settingsMenu = DirectFrame(
            frameColor=(0, 0, 0, 0),
            frameSize=(-1, 1, -1, 1),
            parent=self.base.aspect2d
        )

        self.backdrop = OnscreenImage(
            "../Assets/Images/NeuralNoir_Background_Image.jpg", 
            pos = (1, 0, 0), 
            parent = self.settingsMenu)

        self.backdropBack = OnscreenImage(
            "../Assets/Images/Black.jpg",
            pos = (-1, 0, 0),
            parent = self.settingsMenu
        )
        self.hide()

        self.topText = TextNode('TopText')
        self.topText.setText("Settings")
        self.topText_np = self.settingsMenu.attachNewNode(self.topText)  
        self.topText_np.setScale(0.25)
        self.topText_np.setPos(-1, 0, 0.7)
        self.topText.setAlign(self.topText.ACenter)
        self.topText.font = loader.loadFont(limeLight)

        self.backButton = DirectButton(
            text="Back",
            text_font = loader.loadFont(limeLight),
            text_fg = (1,1,1,1),
            scale=0.1,
            pos=(-1, 0, 0),
            parent=self.settingsMenu,
            command=self.moveToMain,
            frameColor = (0,0,0,0)
        )

        self.audioButton = DirectButton(
            text="Audio",
            text_font = loader.loadFont(limeLight),
            text_fg = (1,1,1,1),
            scale=0.1,
            pos=(-1, 0, 0.3),
            command=self.moveToAudio,
            parent=self.settingsMenu,
            frameColor = (0,0,0,0)
        )

        self.backButton.bind(DGG.ENTER, lambda event: self.setColorHover(self.backButton))  # Mouse enters
        self.backButton.bind(DGG.EXIT, lambda event: self.setColorDefault(self.backButton)) 

        self.audioButton.bind(DGG.ENTER, lambda event: self.setColorHover(self.audioButton))  # Mouse enters
        self.audioButton.bind(DGG.EXIT, lambda event: self.setColorDefault(self.audioButton)) 

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

    def setColorHover (self, button):
        button["text_fg"] = self.hoverColor

    def setColorDefault (self, button):
        button["text_fg"] = self.mainTextColor     

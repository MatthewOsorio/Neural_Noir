from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectFrame, DirectButton, DGG
from panda3d.core import TextNode
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from panda3d.core import TransparencyAttrib

class Tutorial:
    def __init__(self, base):
        self.base = base

        self.tutorialActive = False
    
        self.tutorialFrame = DirectFrame(
            frameColor=(0, 0, 0, 0),
            frameSize=(-1, 1, -1, 1),
            parent=self.base.base.aspect2d
        )

        self.tutorialImage = OnscreenImage(
            self.base.base.menuManager.room,
            parent=self.tutorialFrame,
            scale=(1.5, 0.8, 0.8),
            pos=(0 , 0, 0),
        )

        self.tutorialImage.setColor(0, 0, 0, 0.7)
        self.tutorialImage.setTransparency(TransparencyAttrib.MAlpha)

        self.tutorialPrompt = OnscreenText(
            text = "Tutorial",
            #font = loader.loadFont("../Assets/Fonts/Limelight/Limelight-Regular.ttf"),
            scale = (0.05, 0.05, 0.05),
            wordwrap=35,
            parent = self.tutorialFrame,
            fg = (1,1,1,1),
            pos = (0,0,0)
        )

        self.tutorialButton = DirectButton(
            text="OK",
            text_font = self.base.menu.font,
            text_fg = (1,1,1,1),
            scale=0.1,
            pos=(-1, -0.7, -0.7),
            command=self.setInactive,
            parent=self.tutorialFrame,
            frameColor = (0,0,0,0)
        )

        self.hideTutorialBox()

    
    def moveBox(self, position, scale):
        self.tutorialImage.setPos(position)
        self.tutorialImage.setScale(scale)
    
    def setText(self, text, position, scale, wordWrap):
        self.tutorialPrompt.setText(text)
        self.tutorialPrompt.setPos(*position)
        self.tutorialPrompt.setWordwrap(wordWrap)

    def hideTutorialBox(self):
        self.tutorialFrame.hide()

    def showTutorialBox(self, showButton):
        self.tutorialFrame.show()
        if showButton == False:
            self.tutorialButton.hide()
        elif showButton == True:
            self.tutorialButton.show()

    def setInactive(self):
        self.tutorialActive = False

    def getActive(self):
        return self.tutorialActive
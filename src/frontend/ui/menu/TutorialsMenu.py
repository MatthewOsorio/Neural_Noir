from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectFrame, DirectButton, DGG
from panda3d.core import TextNode
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *

from ..menu.emotibitSetUp import EmotibitTutorial


class TutorialsMenu:
    def __init__(self, manager, base):
        self.manager = manager
        self.base = base

        self.eTutorial = EmotibitTutorial(self.base, self.manager)

        self.tutorialsMenu = DirectFrame(
            frameColor=(0, 0, 0, 0),
            frameSize=(-1, 1, -1, 1),
            parent=self.base.aspect2d
        )

        self.backdrop = OnscreenImage(
            self.manager.mainBackground, 
            pos = (1, 0, 0), 
            parent = self.tutorialsMenu
            )

        self.backdropBack = OnscreenImage(
            self.manager.black,
            pos = (-1, 0, 0),
            parent = self.tutorialsMenu
            )


        self.topText = TextNode('TopText')
        self.topText.setText("Tutorials")
        self.topText_np = self.tutorialsMenu.attachNewNode(self.topText)  
        self.topText_np.setScale(0.25)
        self.topText_np.setPos(-1, 0, 0.7)
        self.topText.setAlign(self.topText.ACenter)
        self.topText.font = self.manager.font

        self.startButton = DirectButton(
            text="Gameplay Tutorial",
            text_font = self.manager.font,
            scale=0.1,
            pos=(-1, 0, 0.3),
            parent=self.tutorialsMenu,
            command = self.loadTutorialRoom,
            frameColor = (0, 0, 0, 0.0),
            text_fg = (1, 1, 1, 1)
        )

        self.emotibitTutorialButton = DirectButton(
            text = "EmotiBit Tutorial",
            text_font = self.manager.font,
            scale = 0.1,
            pos=(-1, 0, 0.0),
            parent = self.tutorialsMenu,
            command = self.loadEmotiBitTutorial,
            frameColor = (0, 0, 0, 0.0),
            text_fg = (1, 1, 1, 1)
        )

        self.backButton = DirectButton(
            text="Back",
            text_font = self.manager.font,
            text_fg = (1,1,1,1),
            scale=0.1,
            pos=(-1, -0.9, -0.9),
            parent=self.tutorialsMenu,
            command=self.moveToMain,
            frameColor = (0, 0, 0, 0.0),
        )

        self.setButtonHovers()
        self.hide()
        self.eTutorial.hide()

    def moveToMain(self):
        self.hide()
        self.manager.showMain()
    
    def hide(self):
        self.tutorialsMenu.hide()

    def show(self):
        self.tutorialsMenu.show()
    
    def loadTutorialRoom(self):
        self.hide()
        self.manager.hideImage()
        self.manager.beginTutorial()

    def loadEmotiBitTutorial(self):
        self.hide()
        self.eTutorial.show()
        self.eTutorial.setUpBC()
        self.eTutorial.button['command'] = self.hideEmotiBitTutorial
    
    def hideEmotiBitTutorial(self):
        self.eTutorial.goBack()
        self.show()
    
    def setButtonHovers(self):
        self.startButton.bind(DGG.ENTER, lambda event: self.manager.setColorHover(self.startButton)) 
        self.startButton.bind(DGG.EXIT, lambda event: self.manager.setColorDefault(self.startButton)) 

        self.emotibitTutorialButton.bind(DGG.ENTER, lambda event: self.manager.setColorHover(self.emotibitTutorialButton)) 
        self.emotibitTutorialButton.bind(DGG.EXIT, lambda event: self.manager.setColorDefault(self.emotibitTutorialButton)) 

        self.backButton.bind(DGG.ENTER, lambda event: self.manager.setColorHover(self.backButton)) 
        self.backButton.bind(DGG.EXIT, lambda event: self.manager.setColorDefault(self.backButton)) 

    def updateFont(self):
        self.startButton["text_font"] = self.manager.font
        self.emotibitTutorialButton["text_font"] = self.manager.font
        self.backButton["text_font"] = self.manager.font
        self.topText.font = self.manager.font
        self.updateEmotibitTutorialFont()

    def updateEmotibitTutorialFont(self):
        self.eTutorial.updateFonts()
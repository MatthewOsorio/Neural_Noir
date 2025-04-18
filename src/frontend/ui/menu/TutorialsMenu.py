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

        self.eTutorial = EmotibitTutorial(self.base)

        self.tutorialsMenu = DirectFrame(
            frameColor=(0, 0, 0, 0),
            frameSize=(-1, 1, -1, 1),
            parent=self.base.aspect2d
        )

        self.startButton = DirectButton(
            text="Gameplay Tutorial",
            text_font = self.manager.font,
            scale=0.1,
            pos=(-1, 0, 0.3),
            parent=self.tutorialsMenu,
            command = self.loadTutorialRoom
        )

        self.emotibitTutorialButton = DirectButton(
            text = "EmotiBit Tutorial",
            text_font = self.manager.font,
            scale = 0.1,
            pos=(-1, 0, 0.5),
            parent = self.tutorialsMenu,
            command = self.loadEmotiBitTutorial
        )

        self.backButton = DirectButton(
            text="Back",
            text_font = self.manager.font,
            text_fg = (1,1,1,1),
            scale=0.1,
            pos=(-1, -0.9, -0.9),
            parent=self.tutorialsMenu,
            command=self.moveToMain
        )

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
    
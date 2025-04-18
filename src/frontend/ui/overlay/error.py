from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectFrame, DirectButton, DGG
from panda3d.core import TextNode
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
import sys


class ErrorScreen:
    def __init__(self, base):
        self.base = base

        self.connectionError = DirectFrame(
            frameColor=(0, 0, 0, 0),
            frameSize=(-1, 1, -1, 1),
            parent=self.base.base.aspect2d
        )

        self.connectionErrorBG = OnscreenImage(
            self.base.base.menuManager.black,
            parent=self.connectionError,
            scale=(2, 2, 2),
            pos=(0 , 0, 0)
        )

        self.connectionErrorText = OnscreenText(
            text = "Connection Error",
            font = loader.loadFont("../Assets/Fonts/Limelight/Limelight-Regular.ttf"),
            scale = 0.2,
            parent = self.connectionError,
            fg = (1,1,1,1),
            pos = (0,0.6,0)
        )

        self.connectionErrorText2 = OnscreenText(
            text = "Please check your internet connection.",
            font = loader.loadFont("../Assets/Fonts/Limelight/Limelight-Regular.ttf"),
            scale = 0.1,
            parent = self.connectionError,
            fg = (1,1,1,1),
            pos = (0,0.4,0)
        )

        self.connectionErrorButton = DirectButton(
            text = "Quit Game",
            text_font = loader.loadFont("../Assets/Fonts/Limelight/Limelight-Regular.ttf"),
            scale = 0.1,
            frameColor = (1, 1, 1, 1),
            parent = self.connectionError,
            pos = (0, 0, 0),
            command = self.closeGame,
            sortOrder=3
        )

        self.connectionErrorBG.setBin("fixed", 2)
        self.connectionErrorText.setBin("fixed", 3)
        self.connectionErrorText2.setBin("fixed", 3)

    def showConnectionError(self):
        self.connectionError.show()
    
    def hideConnectionError(self):
        self.connectionError.hide()

    def closeGame(self):
        sys.exit()
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectLabel import DirectLabel
from direct.gui.DirectScrolledFrame import DirectScrolledFrame
from panda3d.core import TextNode

class Subtitles:
    def __init__(self, manager, gameController, interrogationRoomResponse):
        self.manager = manager
        self.gameController = gameController
        self.interrogationRoomResponse = interrogationRoomResponse
        self.subtitleDisplay = None
        self.generateSubtitleBox()
    
    def getCurrentResponse(self):
        return self.interrogationRoomResponse.runInterrogation()

    def generateSubtitleBox(self):

        self.subtitleDisplay = DirectFrame(
            frameColor=(0, 0, 0, 0.7),
            frameSize=(-1.5, 1.5, -0.3, 0.3),
            pos=(0, 0, -0.7)
        )

        subtitleText = self.getCurrentResponse()

        self.textDisplay = DirectLabel(
            parent=self.subtitleDisplay,
            text=subtitleText,
            text_align=TextNode.ALeft,
            text_scale=0.05,
            pos=(-1.4, 0, 0.1),
            frameColor=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
            text_wordwrap=40
        )

    def showSubtitles(self):
        self.subtitleDisplay.show()

    def hideSubtitles(self):
        self.subtitleDisplay.hide()
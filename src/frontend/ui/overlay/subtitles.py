from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectLabel import DirectLabel
from direct.gui.DirectScrolledFrame import DirectScrolledFrame
from direct.gui.OnscreenText import OnscreenText

from panda3d.core import TextNode

#Class originally by Christine
class Subtitles:
    def __init__(self, base):
        self.base = base
        self.response = None

        self.subtitles = OnscreenText(
            text = "Subtitles",
            #font = loader.loadFont("../Assets/Fonts/Limelight/Limelight-Regular.ttf"),
            scale = (0.05, 0.15, 0.15),
            wordwrap=35,
            parent = None,
            fg = (1,1,1,1),
            pos = (0,0,0)
        )
    
    def setResponse(self, response):
        self.response = response
    
    def setParent(self, parent):
        self.subtitles.reparentTo(parent)

    def showSubtitles(self):
        self.subtitles.show()

    def hideSubtitles(self):
        self.subtitles.hide()

    #Updates the subtitles to the response from the detective 
    #Will be moved into its own class
    def updateSubtitles(self):
        self.subtitles.setText(self.response)
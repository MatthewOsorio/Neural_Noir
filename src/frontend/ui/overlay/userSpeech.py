from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectLabel import DirectLabel
from direct.gui.DirectGui import DirectFrame, DirectButton, DGG
from direct.gui.DirectScrolledFrame import DirectScrolledFrame
from direct.gui.OnscreenText import OnscreenText

from panda3d.core import TextNode

class UserSpeech:
    def __init__(self, base):
        self.base = base
        self.speech = None

        self.button = None
        self.active = False
        self.redo = False

        self.speechText = OnscreenText(
            text = "speech",
            #font = loader.loadFont("../Assets/Fonts/Limelight/Limelight-Regular.ttf"),
            scale = (0.05, 0.15, 0.15),
            wordwrap=35,
            parent = None,
            fg = (1,1,1,1),
            pos = (0,0,0)
        )

    def setSpeech(self, response):
        self.speech = response
        self.updateSpeechText()
    
    def setParent(self, parent):
        self.speechText.reparentTo(parent)

    def showSpeech(self):
        self.speechText.show()

    def hideSpeech(self):
        self.speechText.hide()

    def setButton(self, button):
        self.button = button
    
    def setInactive(self):
        self.active = False
        self.redo = False
    
    def setInactiveSignalRedo(self):
        self.active = False
        self.redo = True
    
    def getActive(self):
        return self.active

    #Updates the subtitles to the response from the detective 
    #Will be moved into its own class
    def updateSpeechText(self):
        self.speechText.setText(self.speech)
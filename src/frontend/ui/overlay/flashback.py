from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectFrame, DirectButton, DGG
from panda3d.core import TextNode
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *

#Use this to show evidence or other images during the gameplay

class flashback:
    def __init__(self, base):
        self.base = base

        self.active = False

        self.flashback = DirectFrame(
            frameColor=(0, 0, 0, 0),
            frameSize=(-1, 1, -1, 1),
            parent=self.base.base.aspect2d
        )

        self.flashbackImage = OnscreenImage(
            self.base.base.menuManager.room,
            parent=self.flashback,
            scale=(1.5, 0.8, 0.8),
            pos=(0 , 0, 0),
        )

        self.nextButton = DirectButton(
            text = "Next",
            #text_fg = (1,1,1,1),
            text_font = loader.loadFont("../Assets/Fonts/Limelight/Limelight-Regular.ttf"),
            scale = 0.1,
            frameColor = (1, 1, 1, 1),
            parent = self.flashback,
            pos = (1.5, 1, -0.8),
            command = self.hide,
            sortOrder=1
        )

        self.hide()

    #Please specify the image path in the folder calling this function
    def setImage(self, image):
        self.flashbackImage.setImage(image)

    def show(self):
        self.flashback.show()
        self.active = True
    
    def hide(self):
        self.flashback.hide()
        self.active = False
    
    #You can use to check if the flashback is currently active. Use while loop to halt other game processes until flashback image is closed (via button press)
    def getActive(self):
        return self.active
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectFrame, DirectButton, DGG
from panda3d.core import TextNode
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
import time
from direct.task import Task
from direct.interval.LerpInterval import LerpPosInterval

class EmotibitTutorial:
    def __init__(self, base, manager):
        self.base = base
        self.manager = manager
        self.active = False
        self.wordWrap = 50

        self.frame = DirectFrame(
            frameColor=(0, 0, 0, 1),
            frameSize=(-2, 2, -2, 2),
            parent=self.base.aspect2d
        )

        self.button = DirectButton(
            text="Back",
            scale=0.1,
            command=None,
            pos=(0, 0, -0.9),
            parent=self.frame,
            text_fg = (1, 1, 1, 1),
            frameColor = (0, 0, 0, 0.8),
            text_font = self.manager.font
        )

        self.button.bind(DGG.ENTER, lambda event: self.setColorHover(self.button))  
        self.button.bind(DGG.EXIT, lambda event: self.setColorDefault(self.button)) 

        self.mainTextColor = (1,1,1,1)
        self.hoverColor = (1,1,0.5,1)

        self.etTop = OnscreenText(
            text = "EmotiBit Set Up",
            scale = 0.1,
            pos = (0, 0.7, 0.7),
            parent = self.frame,
            fg = (1, 1, 1, 1)
        )

        self.et = OnscreenText()
        self.errorText = OnscreenText()

        self.warningTextCreator(
            self.et, 
            "Players who own an EmotiBit can use it to read their biometric data during gameplay. This game requires users connect to their EmotiBit via wifi connection." \
            "To connect your EmotiBit to your wifi, follow these steps:\n\n\n\n" 
            "          1. Remove the microSD card from the base of the EmotiBit.\n" 
            "          2. Insert the microSD card into your computer.\n" 
            "          3. Locate the microSD card in your files, and open 'Config.txt.'\n"
            "          4. Change the SSID and password to match your network.\n"
            "          5. Safely remove the microSD card and reinsert it into the base of the EmotiBit.\n\n\n\n"
            "If you are playing with EmotiBit mode on, you should have the EmotiBit set up and connected before starting the game. Wearing the EmotiBit on your wrist is optimal.\n\n"
            "For more help with setting up the EmotiBit, please see the EmotiBit documentation: https://github.com/EmotiBit/EmotiBit_Docs\n\n",
            (0, 0.3), 0.05, self.frame, (1, 1, 1, 1))
  
        self.etTop.setFont(self.manager.font)
        
    def show(self):
        self.active = True
        self.frame.show()
    
    def hide(self):
        self.active = False
        self.frame.hide()

    def warningTextCreator(self, item, text, pos, scale, parent, color):
        item = OnscreenText(
            text=text,
            pos=pos,
            scale=scale,
            parent=parent,
            fg=color,
            wordwrap= self.wordWrap
        )

    
    def show(self):
        self.frame.show()
    
    def hide(self):
        self.frame.hide()
    
    def cleanUp(self):
        pass

    def goBack(self):
        self.cleanUp()
        self.hide()

    def setUpBC(self):
        pass

    def setColorHover (self, button):
        button["text_fg"] = self.hoverColor

    def setColorDefault (self, button):
        button["text_fg"] = self.mainTextColor

    def updateFonts(self):
        self.etTop.setFont(self.manager.font)
        self.button["text_font"] = self.manager.font
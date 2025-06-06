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

class Warning:
    def __init__(self, base):
        self.base = base
        self.active = False
        self.wordWrap = 50

        self.frame = DirectFrame(
            frameColor=(0, 0, 0, 1),
            frameSize=(-2, 2, -2, 2),
            parent=self.base.aspect2d
        )

        self.button = DirectButton(
            text="I understand",
            scale=0.05,
            command=None,
            pos=(0, 0, -0.6),
            parent=self.frame,
            frameColor = (0, 0, 0, 0),
            text_fg = (1, 1, 1, 1)
        )

        self.button.bind(DGG.ENTER, lambda event: self.setColorHover(self.button))  # Mouse enters
        self.button.bind(DGG.EXIT, lambda event: self.setColorDefault(self.button)) 

        self.warningTextTop = OnscreenText
        self.warningTextAIUsage = OnscreenText
        self.warningTextNLP = OnscreenText
        self.warningTextBiometricData = OnscreenText

        self.warningTextCreator(self.warningTextTop, "Notice", (0, 0.8), 0.1, self.frame, (1, 1, 1, 1))
        self.warningTextCreator(
            self.warningTextAIUsage, 
            "This game uses OpenAI's ChatGPT to generate responses. By continuing, you agree to the use of generative AI technology.", 
            (0, 0.5), 0.05, self.frame, (1, 1, 1, 1))
        self.warningTextCreator(
            self.warningTextNLP, 
            "This game uses speech input. Your replies will be stored locally on your computer for viewing purposes, they are not stored remotely"
            ". However, they are used by ChatGPT to generate replies. " \
            "Please refrain from using sensitive information. "
            "To find out more about OpenAI's data usage policy, visit: https://openai.com/policies/usage-policies/", 
            (0, 0.3), 0.05, self.frame, (1, 1, 1, 1))
        self.warningTextCreator(
            self.warningTextBiometricData,
            "Biometric data can be used to influence the game's progression. Biometric data is not stored nor is it directly used by ChatGPT." \
            "You can opt out of using biometric data in the settings menu.\nPress 'I understand' to continue",
            (0, 0), 0.05, self.frame, (1, 1, 1, 1))
        
        

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

    def setColorHover (self, button):
        button["text_fg"] = (1, 1, 0.5, 1)

    def setColorDefault (self, button):
        button["text_fg"] = (1, 1, 1, 1)

        
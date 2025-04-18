from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectFrame, DirectButton, DGG
from panda3d.core import TextNode
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
import json

class settingsMenu:
    def __init__(self, manager, base):
        self.base = base
        self.manager = manager

        self.mainTextColor = (1,1,1,1)
        self.hoverColor = (1,1,0.5,1)

        self.useEmotibit = False
        self.difficulty = "easy"

        self.settingsMenu = DirectFrame(
            frameColor=(0, 0, 0, 0),
            frameSize=(-1, 1, -1, 1),
            parent=self.base.aspect2d
        )

        self.backdrop = OnscreenImage(
            self.manager.mainBackground, 
            pos = (1, 0, 0), 
            parent = self.settingsMenu)

        self.backdropBack = OnscreenImage(
            self.manager.black,
            pos = (-1, 0, 0),
            parent = self.settingsMenu
        )
        self.hide()

        self.topText = TextNode('TopText')
        self.topText.setText("Settings")
        self.topText_np = self.settingsMenu.attachNewNode(self.topText)  
        self.topText_np.setScale(0.25)
        self.topText_np.setPos(-1, 0, 0.7)
        self.topText.setAlign(self.topText.ACenter)
        self.topText.font = self.manager.font

        self.useEmotibitText = OnscreenText(
            text = 'Use Emotibit',
            font = self.manager.font,
            scale = 0.1,
            parent = self.settingsMenu,
            fg = (1,1,1,1),
            pos = (-1, 0.4 ,0)
        )

        self.emotibitOn = DirectCheckButton(
            text = "On",
            text_font = self.manager.font,
            parent = self.settingsMenu,
            scale = 0.1,
            pos = (-1.3, 0.3, 0.25),
            command = self.setEmotibitOn
        )

        self.emotibitOff = DirectCheckButton(
            text = "Off",
            text_font = self.manager.font,
            parent = self.settingsMenu,
            scale = 0.1,
            pos = (-0.7, 0.3, 0.25),
            command = self.setEmotibitOff
        )

        self.difficultyText = OnscreenText(
            text = 'Difficulty',
            font = self.manager.font,
            scale = 0.1,
            parent = self.settingsMenu,
            fg = (1,1,1,1),
            pos = (-1, 0.1 ,0)
        )

        self.difficultyDesc = OnscreenText(
            text = 'Playing on hard mode will remove some of the hints, \nand you will not know if your biometric data is in the normal range.' \
            '\nAlso, the amount of evidence you need to successfully refute will be higher.',
            scale = 0.04,
            parent = self.settingsMenu,
            fg = (1,1,1,1),
            pos = (-1, 0.03 ,0.03)
        )

        self.diffEasy = DirectCheckButton(
            text = "Easy",
            text_font = self.manager.font,
            parent = self.settingsMenu,
            scale = 0.1,
            pos = (-1.3, 0.0, -0.2),
            command = self.setDifficultyEasy
        )

        self.diffHard = DirectCheckButton(
            text = "Hard",
            text_font = self.manager.font,
            parent = self.settingsMenu,
            scale = 0.1,
            pos = (-0.7, 0.0, -0.2),
            command = self.setDifficultyHard
        )

        self.fontText = OnscreenText(
            text = 'Font',
            font = self.manager.font,
            scale = 0.1,
            parent = self.settingsMenu,
            fg = (1,1,1,1),
            pos = (-1, -0.3 , -0.3)
        )

        self.fontStylized = DirectCheckButton(
            text = "Stylized",
            text_font = self.manager.font,
            parent = self.settingsMenu,
            scale = 0.1,
            pos = (-1.3, -0.4, -0.4),
            command = self.setFontLime
        )

        self.fontNormal = DirectCheckButton(
            text = "Normal",
            text_font = self.manager.font,
            parent = self.settingsMenu,
            scale = 0.1,
            pos = (-0.7, -0.4, -0.4),
            command = self.setFontNormal
        )

        self.backButton = DirectButton(
            text="Back",
            text_font = self.manager.font,
            text_fg = (1,1,1,1),
            scale=0.1,
            pos=(-1, -0.9, -0.9),
            parent=self.settingsMenu,
            command=self.moveToMain,
            frameColor = (0,0,0,0)
        )

        self.audioButton = DirectButton(
            text="Audio",
            text_font = self.manager.font,
            text_fg = (1,1,1,1),
            scale=0.1,
            pos=(-1, -0.7, -0.7),
            command=self.moveToAudio,
            parent=self.settingsMenu,
            frameColor = (0,0,0,0)
        )

        self.backButton.bind(DGG.ENTER, lambda event: self.setColorHover(self.backButton))  # Mouse enters
        self.backButton.bind(DGG.EXIT, lambda event: self.setColorDefault(self.backButton)) 

        self.audioButton.bind(DGG.ENTER, lambda event: self.setColorHover(self.audioButton))  # Mouse enters
        self.audioButton.bind(DGG.EXIT, lambda event: self.setColorDefault(self.audioButton)) 

        with open(self.manager.userSettings, "r", encoding="utf-8") as file:
            settings = json.load(file)

        self.setUserSettingsValues(settings)

    def moveToMain(self):
        self.hide()
        self.manager.showMain()

    def moveToAudio(self):
        self.hide()
        self.manager.showAudio()

    def show(self):
        self.settingsMenu.show()
        
    def hide(self):
        self.settingsMenu.hide()

    def setColorHover (self, button):
        button["text_fg"] = self.hoverColor

    def setColorDefault (self, button):
        button["text_fg"] = self.mainTextColor     

    def setEmotibitOn(self, state):
        self.useEmotibit = True
        self.emotibitOff["indicatorValue"] = False
        self.emotibitOn["indicatorValue"] = True
        self.emotibitOff.setIndicatorValue
        self.emotibitOn.setIndicatorValue

        with open(self.manager.userSettings, "r", encoding="utf-8") as file:
            settings = json.load(file)
        settings["emotibit"] = True
        with open(self.manager.userSettings, 'w') as file:
            json.dump(settings, file)
    
    def setEmotibitOff(self, state):
        self.useEmotibit = False
        self.emotibitOn["indicatorValue"] = False
        self.emotibitOff["indicatorValue"] = True
        self.emotibitOn.setIndicatorValue
        self.emotibitOff.setIndicatorValue
        
        with open(self.manager.userSettings, "r", encoding="utf-8") as file:
            settings = json.load(file)
        settings["emotibit"] = False
        with open(self.manager.userSettings, 'w') as file:
            json.dump(settings, file)
    
    def setDifficultyEasy(self, state):
        self.difficulty = "easy"
        self.diffHard["indicatorValue"] = False
        self.diffEasy["indicatorValue"] = True
        self.diffHard.setIndicatorValue
        self.diffEasy.setIndicatorValue

        with open(self.manager.userSettings, "r", encoding="utf-8") as file:
            settings = json.load(file)
        settings["difficulty"] = "easy"
        with open(self.manager.userSettings, 'w') as file:
            json.dump(settings, file)

    def setDifficultyHard(self, state):
        self.difficulty = "hard"
        self.diffHard["indicatorValue"] = True
        self.diffEasy["indicatorValue"] = False
        self.diffHard.setIndicatorValue
        self.diffEasy.setIndicatorValue

        with open(self.manager.userSettings, "r", encoding="utf-8") as file:
            settings = json.load(file)
        settings["difficulty"] = "hard"
        with open(self.manager.userSettings, 'w') as file:
            json.dump(settings, file)

    def setFontLime(self, state):
        self.manager.setFontLime()
        self.fontStylized["indicatorValue"] = True
        self.fontNormal["indicatorValue"] = False
        self.fontStylized.setIndicatorValue
        self.fontNormal.setIndicatorValue
        with open(self.manager.userSettings, "r", encoding="utf-8") as file:
            settings = json.load(file)
        settings["font"] = "stylized"
        with open(self.manager.userSettings, 'w') as file:
            json.dump(settings, file)        

    def setFontNormal(self, state):
        self.manager.setFontNormal()
        self.fontStylized["indicatorValue"] = False
        self.fontNormal["indicatorValue"] = True
        self.fontStylized.setIndicatorValue
        self.fontNormal.setIndicatorValue
        with open(self.manager.userSettings, "r", encoding="utf-8") as file:
            settings = json.load(file)
        settings["font"] = "normal"
        with open(self.manager.userSettings, 'w') as file:
            json.dump(settings, file)   

    def getUseEmotibit(self):
        return self.useEmotibit
    
    def getDifficulty(self):
        return self.difficulty

    def setUserSettingsValues(self, settings):
        self.settings = settings
        if self.settings["emotibit"] == True:
            self.setEmotibitOn(True)
        elif self.settings["emotibit"] == False:
            self.setEmotibitOff(True)
        if self.settings["difficulty"] == "easy":
            self.setDifficultyEasy(True)
        elif self.settings["difficulty"] == "hard":
            self.setDifficultyHard(True)
        if self.settings["font"] == "stylized":
            self.setFontLime(True)
        elif self.settings["font"] == "normal":
            self.setFontNormal(True)
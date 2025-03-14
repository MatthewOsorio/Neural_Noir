from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectFrame, DirectButton, DGG
from panda3d.core import TextNode
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from panda3d.core import TransparencyAttrib
import json

class audioSettings:
    def __init__(self, manager, base, audio, back_callback=None):    

        self.base = base
        self.back_callback = back_callback
        self.audio = audio
        self.manager = manager

        self.audioMenu = DirectFrame(
            frameColor=(0, 0, 0, 0), 
            frameSize=(-1, 1, -1, 1), 
            parent=self.base.aspect2d
        )

        self.backImage = OnscreenImage(
            self.manager.black,
            parent=self.audioMenu,
            scale=(1.5, 0.975, 0.975),
            pos=(0, 0, 0)
        )

        self.backImage.setColor(0, 0, 0, 0.5)
        self.backImage.setTransparency(TransparencyAttrib.MAlpha)

        self.topText = TextNode('TopText')
        self.topText.setText("Audio Settings")
        self.topText_np = self.audioMenu.attachNewNode(self.topText)
        self.topText_np.setScale(0.2)
        self.topText_np.setPos(0, 0, 0.8)
        self.topText.setWordwrap(25.0)
        self.topText.setAlign(self.topText.ACenter)
        self.topText.font = self.manager.font

        self.volumeText = OnscreenText(
            text = 'Sfx Volume',
            font = self.manager.font,
            scale = 0.15,
            parent = self.audioMenu,
            fg = (1,1,1,1),
            pos = (0,0.5,0.5)
        )

        self.volumeSlider = DirectSlider(
            range=(0,1),
            pageSize = 20,
            pos=(0, 0.4, 0.4),
            scale=0.5,
            parent = self.audioMenu,
            value=0.5,
            command=self.setVolumeV
        )

        self.voiceVolumeText = OnscreenText(
            text = 'Dialogue Volume',
            font = self.manager.font,
            scale = 0.15,
            parent = self.audioMenu,
            fg = (1,1,1,1),
            pos = (0,0.2,0.2)
        )

        self.voiceVolumeSlider = DirectSlider(
            range=(0,1),
            pageSize = 20,
            pos=(0, 0.1, 0.1),
            scale=0.5,
            parent = self.audioMenu,
            value=0.5,
            command=self.setVoiceVolumeV
        )

        self.subTitlesText = OnscreenText(
            text = 'Subtitles',
            font = self.manager.font,
            scale = 0.15,
            parent = self.audioMenu,
            fg = (1,1,1,1),
            pos = (0, -0.2 ,-0.3)
        )

        self.subTitlesOn = DirectCheckButton(
            text = "On",
            text_font = self.manager.font,
            parent = self.audioMenu,
            scale = 0.1,
            pos = (-0.3, -0.3, -0.4),
            command = self.turnSubtitlesOn
        )

        self.subTitlesOff = DirectCheckButton(
            text = "Off",
            text_font = self.manager.font,
            parent = self.audioMenu,
            scale = 0.1,
            pos = (0.4, -0.3, -0.4),
            command = self.turnSubtitlesOff
        )

        self.backButton = DirectButton(
            text = ("Back"),
            text_font = self.manager.font,
            scale = 0.12,
            pos = (0,0,-0.7),
            parent = self.audioMenu,
            command = self.handleBack
        )

        self.testInput = DirectButton(
            text = ("Test Microphone"),
            text_font = self.manager.font,
            scale = 0.1,
            pos = (-0.6,0,-0.9),
            parent = self.audioMenu,
            command = self.audio.testAudioInput
        )

        self.testOutput = DirectButton(
            text = ("Test Speakers"),
            text_font = self.manager.font,
            scale = 0.1,
            pos = (0.6,0,-0.9),
            parent = self.audioMenu,
            command = self.audio.testAudioOutput
        )

        with open(self.manager.userSettings, "r", encoding="utf-8") as file:
            settings = json.load(file)

        if settings["subtitles"] == True:
            self.turnSubtitlesOn(True)
        else:
            self.turnSubtitlesOff(True)

        self.setInitialValues(settings)

        self.hide()

    def handleBack(self):
        if self.back_callback:
            self.hide()
            self.back_callback()
        else:
            self.hide()
            self.moveToSettings()

    def moveToSettings(self):
        self.hide()
        self.manager.showSettings()

    def show(self):
        self.audioMenu.show()
        if self.base.interrogationRoom != None:
            self.setVoiceVolumeSlider(self.base.interrogationRoom.voiceVolume)
            self.setSFXVolumeSlider(self.base.interrogationRoom.sfxVolume)

    def hide(self):
        self.audioMenu.hide()

    def setVolumeV(self):
        self.audio.setVolumeValue(self.volumeSlider['value'])
        if self.manager.gameStart == True:
            self.base.interrogationRoom.sfxVolume = self.volumeSlider['value']
        else:
            self.base.sfxVolume = self.volumeSlider['value']

        with open(self.manager.userSettings, "r", encoding="utf-8") as file:
            settings = json.load(file)
        settings["sfxVolume"] = self.volumeSlider['value']
        with open(self.manager.userSettings, "w", encoding="utf-8") as file:
            json.dump(settings, file)

    def setVoiceVolumeV(self):
        if self.manager.gameStart == True:
            self.base.interrogationRoom.game._tts.audio.setVolume(self.voiceVolumeSlider['value'])
            self.base.interrogationRoom.voiceVolume = self.voiceVolumeSlider['value']
        else:
            self.base.voiceVolume = self.voiceVolumeSlider['value']
        

        with open(self.manager.userSettings, "r", encoding="utf-8") as file:
            settings = json.load(file)
        settings["voiceVolume"] = self.voiceVolumeSlider['value']
        with open(self.manager.userSettings, "w", encoding="utf-8") as file:
            json.dump(settings, file)
            
    def turnSubtitlesOn(self, state):
        self.subTitlesOff["indicatorValue"] = False
        self.subTitlesOff.setIndicatorValue
        self.manager.subtitles = True

        with open(self.manager.userSettings, "r", encoding="utf-8") as file:
            settings = json.load(file)
        settings["subtitles"] = True
        with open(self.manager.userSettings, "w", encoding="utf-8") as file:
            json.dump(settings, file)
    
    def turnSubtitlesOff(self, state):
        self.subTitlesOn["indicatorValue"] = False
        self.subTitlesOn.setIndicatorValue
        self.manager.subtitles = False

        with open(self.manager.userSettings, "r", encoding="utf-8") as file:
            settings = json.load(file)
        settings["subtitles"] = False
        with open(self.manager.userSettings, "w", encoding="utf-8") as file:
            json.dump(settings, file)

    def setVoiceVolumeSlider(self, value):
        self.voiceVolumeSlider["value"] = value 
        self.voiceVolumeSlider.setValue(value)
        self.base.interrogationRoom.game._tts.audio.setVolume(value)
    
    def setSFXVolumeSlider(self, value):
        self.volumeSlider["value"] = value 
        self.volumeSlider.setValue(value)
        self.audio.setVolumeValue(value)
    
    def setInitialValues(self, settings):
        self.settings = settings
        self.audio.setVolumeValue(self.settings.get("sfxVolume", 0.5))
        self.base.sfxVolume = self.settings.get("sfxVolume", 0.5)
        self.base.voiceVolume = self.settings.get("voiceVolume", 0.5)
        self.voiceVolumeSlider["value"] = self.settings.get("voiceVolume", 0.5) 
        self.voiceVolumeSlider.setValue(self.settings.get("voiceVolume", 0.5))
        self.volumeSlider["value"] = self.settings.get("sfxVolume", 0.5)
        self.volumeSlider.setValue(self.settings.get("sfxVolume", 0.5))


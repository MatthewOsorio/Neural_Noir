from direct.showbase.ShowBase import ShowBase
import pyaudio

class audioManager:
    def __init__(self, base):
        self.base = base

        #Sound effects library 
        self.soundEffects = {
            "testMusic" : self.base.loader.loadSfx('../Assets/Audio/testSong.mp3'),
            "testSound" : self.base.loader.loadSfx('../Assets/Audio/testSound.mp3')
        }

        #self.soundEffects['testSound'].play()

    def setVolumeValue(self, value):
        for self.name, self.sound in self.soundEffects.items():
            self.sound.setVolume(value)

class microphoneTest:
    def __init__(self, base):
        self.base = base
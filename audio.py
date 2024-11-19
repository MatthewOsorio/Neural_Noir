from direct.showbase.ShowBase import ShowBase

class audioManager:
    def __init__(self, base):
        print("Hi")

        self.base = base

        self.soundEffects = {
            "testMusic" : self.base.loader.loadSfx('Assets/Audio/testSong.mp3'),
            "testSound" : self.base.loader.loadSfx('Assets/Audio/testSound.mp3')
        }

        self.soundEffects['testSound'].play()

    def setVolumeValue(self, value):
        print(value)
        for self.name, self.sound in self.soundEffects.items():
            self.sound.setVolume(value)
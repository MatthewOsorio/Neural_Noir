import pygame
import time

class AudioController:
    def __init__(self):
        pygame.mixer.init()
        self.paused = False
        self.mixerExist = True
        self.volume = 1

    def playText(self, path):
        pygame.mixer.music.load(str(path))
        pygame.mixer.music.play()

        self.paused = False

        #Makes sure TTS Controller does not delete the audio file before it finishes playing
        while self.playing() == True or self.paused == True:
            time.sleep(0.1)
        
        pygame.mixer.music.stop()
        
        #File must be unloaded before it can be deleted
        pygame.mixer.music.unload()

    def playing(self):
        if self.mixerExist == True:
            return pygame.mixer.music.get_busy()
    
    def pauseSpeech(self):
        if self.paused == False:
            self.paused = True
            pygame.mixer.music.pause()
            
        #print("audio paused")

    def resumeSpeech(self):
        if self.paused == True:
            pygame.mixer.music.unpause()
            self.paused = False
        #print("audio unpased")

    def endMixer(self):
        pygame.mixer.quit()
        self.mixerExist = False

    def setVolume(self, value):
        self.volume = value
        pygame.mixer.music.set_volume(self.volume)

import pygame

class AudioController:
    def __init__(self):
        pygame.mixer.init()

    def playText(self, path):
        pygame.mixer.music.load(str(path))
        pygame.mixer.music.play()

        #Makes sure TTS Controller does not delete the audio file before it finishes playing
        while self.playing() == True:
            continue
        
        pygame.mixer.music.stop()
        
        #File must be unloaded before it can be deleted
        pygame.mixer.music.unload()

    def playing(self):
        return pygame.mixer.music.get_busy()
from playsound import playsound

class AudioController:
    def __init__(self):
        pass
    def playText(self, path):
        playsound(str(path))
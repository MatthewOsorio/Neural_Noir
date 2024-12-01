from pydub import AudioSegment
from pydub.playback import play


class AudioController:
    def __init__(self):
        pass
    def playText(self, path):
        self.sound = AudioSegment.from_file(str(path))
        self.play = self.sound
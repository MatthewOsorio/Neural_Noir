import unittest
from TTSSystem.AudioComponent import AudioController

class TestAudioComponent(unittest.TestCase):
    
    def setup(self):
        self.audio_component = AudioController()

    def test_playtext(self):
        pass
    
    def test_playing(self):
        pass
    
    def test_pausespeech(self):
        pass
    
    def test_resumespeech(self):
        pass
    
    def test_endmixer(self):
        pass
    
    def test_setvolume(self):
        pass
    
if __name__ == "__main__":
    unittest.main()
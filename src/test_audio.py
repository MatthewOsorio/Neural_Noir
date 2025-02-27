import unittest
from unittest.mock import patch, Mock
from ui.audio import audioManager

class TestAudio(unittest.TestCase):

    @patch("pygame.mixer.Sound")
    def setUp(self, mock_sound):
        self.base = Mock()
        self.audio = audioManager(self.base)

    def test_set_volume_value(self):
        self.volume = 0.1
        self.audio.setVolumeValue(self.volume)
        for sound in self.audio.soundEffects.values():
            sound.set_volume.assert_called_once_with(self.volume)

if __name__ == "__main__":
    unittest.main()
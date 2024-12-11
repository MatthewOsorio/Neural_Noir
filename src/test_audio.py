import unittest
from unittest.mock import patch, Mock
from audio import audioManager

class TestAudio(unittest.TestCase):
    @patch("pygame.mixer.Sound")
    def setUp(self, mock_sound):
        self.mock_base = Mock()
        self.audio = audioManager(self.mock_base)
  
    def test_check_mic_input(self):
        self.audio.audio_detected = True
        self.assertTrue(self.audio.audio_detected)

    def test_check_no_audio(self):
        self.audio.audio_detected = False
        self.assertFalse(self.audio.audio_detected)

    def test_close_dialog(self):
        mock_dialog = Mock()
        self.audio.dialog = mock_dialog
        result = self.audio.close_dialog()
        mock_dialog.destroy.assert_called_once()
        self.assertEqual(self.audio.dialog, None)
        self.assertEqual(result, 0)


    def test_set_volume_value(self):
        mock_sound = Mock()
        self.audio.soundEffects = {"sound1": mock_sound}
        self.audio.setVolumeValue(0.5)
        mock_sound.set_volume.assert_called_once_with(0.5)

if __name__ == "__main__":
    unittest.main()

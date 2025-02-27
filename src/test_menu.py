import unittest
from unittest.mock import Mock
from unittest.mock import patch
from ui.menu.menu import menuManager
from ui.menu.PauseMenu import PauseMenu
from direct.showbase.ShowBase import ShowBase

class testMenu(unittest.TestCase):

    @patch("ui.menu.menu.mainMenu")  
    @patch("ui.menu.menu.settingsMenu")  
    @patch("ui.menu.menu.audioSettings")  
    @patch("ui.menu.menu.PauseMenu")  
    @patch("ui.menu.menu.confirmQuit")  
    @patch("ui.menu.menu.audioManager") 
    def setUp(self, mockAudioManager, mockConfirmQuit, mockPauseMenu, mockAudioSettings, mockSettingsMenu, mockMainMenu):
        self.base = Mock()  
        self.startFlag = False

        self.menuManager = menuManager(self.base, self.startFlag)

    def testInitialization(self):
        self.assertEqual(self.menuManager.gameStart, False)
        self.assertIsNone(self.menuManager.pauseMenu)
        self.assertEqual(self.menuManager.gameState, 'menu')
    
    @patch('ui.menu.menu.PauseMenu')  
    def testInitializePause(self, mockPauseMenu):
        self.menuManager.initializePauseMenu()
        self.assertIsNotNone(self.menuManager.pauseMenu)

if __name__ == '__main__':
    unittest.main()
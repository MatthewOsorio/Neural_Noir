from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectLabel import DirectLabel
from direct.gui.DirectScrolledFrame import DirectScrolledFrame
from direct.gui.DirectButton import DirectButton
from panda3d.core import TextNode
from ui.ScriptDisplay import ScriptDisplay
from ui.audio import audioManager
from ui.menu import audioSettings


# from GameController import GameController
# from ScriptDisplay import ScriptDisplay    
#Pause Menu Screen
class PauseMenu():
    def __init__(self, manager, menu):
        self.manager = manager
        self.menu = menu

        print("Initializing pause menu") # debug
        self.scriptMenu = ScriptDisplay(self, self.manager.game, self)
        print("scriptdisplay instance created") # debug
        self.scriptMenu.hide()

        self.audioSettingsMenu = audioSettings(self.manager.base.menuManager, back_callback=self.show)

        self.titleImage = OnscreenImage(
            image='../images/Room_Backdrop_Blur.png', 
            parent=self.manager.base.render2d
        )

        self.displayPauseMenu()
        self.ended = False

        print("Pause menu initialized") # debug

    def displayPauseMenu(self):
        self.pauseMenu = DirectFrame(
                frameColor=(0, 0, 0, 0),
                frameSize=(-1.5, 1.5, -0.85, 0.85),
                pos=(0, 0, 0),
                parent=self.manager.base.aspect2d
        )
        
        self.title= DirectLabel(
                parent=self.pauseMenu,
                text= "Pause",
                text_scale= (0.110, 0.110),
                pos= (0, 0, 0.767),
                frameColor= (0, 0, 0, 0),
                text_fg = (255, 255, 255, 1))
        
        self.displayScriptButton = DirectButton(
                                            text= "Script",
                                            scale= 0.075,
                                            pos=(0, 0, 0.25),
                                            parent=self.pauseMenu,
                                            command= self.showScriptMenu
                            )
        print("script button initialized") # debug
        
        self.resumeButton = DirectButton(
            text = "Resume",
            scale = 0.075,
            pos = (0, 0, 0.50),
            parent = self.pauseMenu,
            command = self.resumeGame
        )

        self.quitButton = DirectButton(
            text = "Quit",
            scale = 0.075,
            pos = (0, 0, -0.25),
            parent = self.pauseMenu,
            command = self.returnToMain
        )
        
        self.audioButton = DirectButton(
            text = "Audio",
            scale = 0.075,
            pos = (0, 0, 0),
            parent = self.pauseMenu,
            command = self.testAudioSettings
        )

    def show(self):
        self.displayPauseMenu()
        self.manager.gameState = 'script'

    def hide(self):
        self.pauseMenu.hide()

    def showImage(self):
        self.titleImage.show()

    def hideImage(self):
        self.titleImage.hide()

    def showScriptMenu(self):
        print("button clicked") # debug
        self.hide()
        self.scriptMenu.generateDisplayBox()
        self.scriptMenu.show()

    def resumeGame(self):
        self.hide()
        self.hideImage()
        self.manager.gameState = 'gameplay'
        self.manager.game.tts.audio.resumeSpeech()

    def returnToMain(self):
        self.quitClicked = False

        #Ensures quit command is not sent twice 
        if self.quitClicked == False:
            self.quitClicked == True
            self.hide()
            self.hideImage()
            self.manager.gameState = 'gameplay'
            self.manager.unloadModels()
            self.menu.showMain()
            self.menu.showImage()
            self.menu.gameStart = False
            self.manager.base.checkGameStartFlag()
            self.manager.game.database.closeConnection()
            self.manager.game.biometricController.biometricReader.restartBoard()
            self.manager.game.begin = False
            self.ended = True
            self.manager.base.returnToMenu()
        
    def testAudioSettings(self):
        self.hide()
        self.audioSettingsMenu.show()
        
        
        

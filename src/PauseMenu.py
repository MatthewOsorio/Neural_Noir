from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectLabel import DirectLabel
from direct.gui.DirectScrolledFrame import DirectScrolledFrame
from direct.gui.DirectButton import DirectButton
from panda3d.core import TextNode
from ScriptDisplay import ScriptDisplay


# from GameController import GameController
# from ScriptDisplay import ScriptDisplay    
#Pause Menu Screen
class PauseMenu():
    def __init__(self, manager, menu):
        self.manager = manager
        self.menu = menu

        self.scriptMenu = ScriptDisplay(self, self.manager.game)
        self.scriptMenu.hide()

        self.titleImage = OnscreenImage(
            image='../images/Room_Backdrop_Blur.png', 
            parent=self.manager.base.render2d
        )

        self.displayPauseMenu()
        self.ended = False

    def displayPauseMenu(self):
        self.pauseMenu = DirectFrame(
                frameColor=(0, 0, 0, 0),
                frameSize=(-1.5, 1.5, -0.85, 0.85),
                pos=(0, 0, 0))
        
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
                                            pos=(0, 0, 0.50),
                                            parent=self.pauseMenu,
                                            command= self.showScriptMenu
                            )
        
        self.resumeButton = DirectButton(
            text = "Resume",
            scale = 0.075,
            pos = (0, 0, 0.25),
            parent = self.pauseMenu,
            command = self.resumeGame
        )

        self.quitButton = DirectButton(
            text = "Quit",
            scale = 0.075,
            pos = (0, 0, 0),
            parent = self.pauseMenu,
            command = self.returnToMain
        )
        
    def show(self):
        self.pauseMenu.show()
        self.manager.gameState = 'script'

    def hide(self):
        self.pauseMenu.hide()

    def showImage(self):
        self.titleImage.show()

    def hideImage(self):
        self.titleImage.hide()

    def showScriptMenu(self):
        self.hide()
        self.scriptMenu.show()

    def resumeGame(self):
        self.hide()
        self.hideImage()
        self.manager.gameState = 'gameplay'
        self.manager.game.tts.audio.resumeSpeech()

    def returnToMain(self):
        self.hide()
        self.hideImage()
        self.manager.gameState = 'gameplay'
        self.manager.unloadModels()
        self.menu.showMain()
        self.menu.showImage()
        self.menu.gameStart = False
        self.manager.base.checkGameStartFlag()
        self.manager.game.database.closeConnection()
        self.ended = True

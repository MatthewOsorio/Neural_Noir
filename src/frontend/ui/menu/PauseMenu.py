from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectLabel import DirectLabel
from direct.gui.DirectScrolledFrame import DirectScrolledFrame
from direct.gui.DirectButton import DirectButton
from panda3d.core import TransparencyAttrib

from panda3d.core import TextNode
from frontend.ui.ScriptDisplay import ScriptDisplay
from frontend.ui.menu.AudioMenu import audioSettings
from frontend.ui.audio import audioManager

# from GameController import GameController
# from ScriptDisplay import ScriptDisplay    
#Pause Menu Screen
class PauseMenu():
    def __init__(self, manager, base):
        self.manager = manager
        self.base = base
        self.game = None
        self.room = None
        self.paused = False

        self.scriptMenu = None

        self.audioSettingsMenu = audioSettings(self.manager, self.base, self.manager.audio, back_callback=self.show)

        self.titleImage = OnscreenImage(
            image= self.manager.room, 
            parent=self.base.render2d
        )

        self.displayPauseMenu()
        self.ended = False

        print("Pause menu initialized") # debug

    def displayPauseMenu(self):
        self.pauseMenu = DirectFrame(
            frameColor=(0, 0, 0, 0),
            frameSize=(-1.5, 1.5, -0.85, 0.85),
            pos=(0, 0, 0),
            parent=self.base.aspect2d
        )

        self.backImageMain = OnscreenImage(
            self.manager.room,
            parent=self.pauseMenu,
            scale=(1.5, 0.9, 0.9),
            pos=(0, 0, 0)
        )

        self.backImage = OnscreenImage(
            self.manager.black,
            parent=self.pauseMenu,
            scale=(1.5, 0.9, 0.9),
            pos=(0, 0, 0)
        )

        self.backImage.setColor(0, 0, 0, 0.5)
        self.backImage.setTransparency(TransparencyAttrib.MAlpha)
        
        self.title= DirectLabel(
            parent=self.pauseMenu,
            text= "Pause",
            text_scale= (0.110, 0.110),
            text_font = self.manager.font,
            pos= (0, 0, 0.767),
            frameColor= (0, 0, 0, 0),
            text_fg = (255, 255, 255, 1))
        
        self.displayScriptButton = DirectButton(
            text= "Script",
            text_font = self.manager.font,
            scale= 0.075,
            pos=(0, 0, 0.25),
            parent=self.pauseMenu,
            command= self.scriptGet
                            )
        print("script button initialized") # debug
        
        self.resumeButton = DirectButton(
            text = "Resume",
            scale = 0.075,
            text_font = self.manager.font,
            pos = (0, 0, 0.50),
            parent = self.pauseMenu,
            command = self.resumeGame
        )

        self.quitButton = DirectButton(
            text = "Quit to Menu",
            text_font = self.manager.font,
            scale = 0.075,
            pos = (0, 0, -0.25),
            parent = self.pauseMenu,
            command = self.confirmQuitToMain
        )
        
        self.audioButton = DirectButton(
            text = "Audio",
            text_font = self.manager.font,
            scale = 0.075,
            pos = (0, 0, 0),
            parent = self.pauseMenu,
            command = self.testAudioSettings
        )

    def show(self):
        self.displayPauseMenu()
        self.room.gameState = 'script'

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
        self.room.gameState = 'gameplay'
        self.manager.gameState = 'gameplay'
        self.game._tts.audio.resumeSpeech()
        self.room.Overlay.show()
    
    def confirmQuitToMain(self):
        self.hide()
        self.manager.showQuitPause()

    def returnToMain(self):
        self.quitClicked = False

        #Ensures quit command is not sent twice 
        if self.quitClicked == False:
            self.quitClicked == True
            self.hide()
            self.hideImage()
            self.game.gameState = 'gameplay'
            self.room.unloadModels()
            self.manager.showMain()
            self.manager.showImage()
            self.manager.gameStart = False
            self.room.base.checkGameStartFlag()
            #self.game.database.closeConnection()
            self.game.clearEmotibit()
            self.game.begin = False
            self.ended = True
            self.room.base.returnToMenu()
        
    def testAudioSettings(self):
        self.hide()
        self.audioSettingsMenu.show()

    def getGame(self, game):
        self.game = game

    def script(self):
        print("Initializing pause menu") # debug
        self.scriptMenu = ScriptDisplay(self, self.game, self)
        print("scriptdisplay instance created") # debug
        self.scriptMenu.hide()
        
    def scriptGet(self):
        self.script()
        self.showScriptMenu()   
    
    def getRoom(self, room):
        self.room = room
    
        

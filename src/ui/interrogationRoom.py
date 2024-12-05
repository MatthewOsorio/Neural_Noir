from PauseMenu import PauseMenu
import GameController as gc
from NLPSystem.NLPController import NLPController as nlp
from NLPSystem.IntimidatingStyle import IntimidatingSytle
from TTSSystem.TextToSpeechController import TextToSpeechController as ttsc
from SRSystem.SpeechToText import SpeechToText as stt
from DatabaseController import DatabaseController as db

#Code originally written by Christine 
#Modified by Evie 
class InterrogationRoom:
    def __init__(self, base, menu):
        self.base = base
        self.menu = menu

        self.base.disableMouse()
        self.gameState= 'gameplay'

        #pause game if escape is pressed
        self.base.accept('escape', self.pauseGame)

        intimidating = IntimidatingSytle()
        nlpController = nlp(intimidating)
        self.game = gc.GameController(stt(), nlpController, ttsc(), db())       

        #Matt wrote lines 19 - 33
        #Create pause menu but hide it initially
        self.pauseMenu = PauseMenu(self, self.menu)
        self.pauseMenu.hide()
        self.pauseMenu.hideImage()
        
        #Game will not be pausable if it is the user's turn to reply
        self.pausable = True
        
    def pauseGame(self):
        #Requires the game to not be paused, not be on a menu, and not be the player's turn to reply 
        if(self.gameState == 'gameplay' and self.menu.gameState == 'gameplay' and self.pausable == True):
            self.pauseMenu.show()
            self.pauseMenu.showImage()
            self.gameState = 'paused'
            self.game.tts.audio.pauseSpeech()
        if(self.gameState == 'gameplay' and self.menu.gameState == 'gameplay' and self.pausable == False):
            self.base.menuManager.audio.playSound("errorSound")
        
    def cameraSetUp(self):
        #Moved the camera back slightly so that it does not clip the table
        self.base.camera.setPos(0, -0.2 , 0)
        #Test print for the camera position if we need to change it
        #print(self.base.camera.getPos())

        self.cameraSensitivity = 10
        self.horizontal = 0
        self.vertical = 0

        #Updates the camera angle
        self.base.taskMgr.add(self.moveCamera, "Move Camera")

    #Allows users to rotate the camera slightly to "look around"
    def moveCamera(self, base):
        if self.base.mouseWatcherNode.hasMouse():
            self.x = self.base.mouseWatcherNode.getMouseX()
            self.y = self.base.mouseWatcherNode.getMouseY()

            #X value multiplied by -1 so that the horizontal camera movement is not inverted
            self.horizontal = (self.x * self.cameraSensitivity) * -1
            self.vertical = self.y * self.cameraSensitivity

            self.base.camera.setHpr(self.horizontal, self.vertical, 0)

            #Test for x and y coordinates 
            #print("X: ", self.x, " ", "Y: ", self.y)

        return base.cont
      
    def loadModels(self):
        # Load the room model
        self.room = self.base.loader.loadModel("../blender/converted_room_whole/room.bam")
        self.room.reparentTo(self.base.render)
        self.room.setScale(1)
        self.room.setPos(5.6, 6, 0.2)
        self.room.setHpr(0, 0, 0)

    def unloadModels(self):
        self.room.detachNode()
        self.room.removeNode()
        self.room = None
        #print("Unload models")

    #Run on separate thread
    def runInterrogation(self):
        
        self.game.startInterrogation()
        self.end = False
        while self.end==False:
           
            #print("Playing")
            self.pausable = False
            speech = self.game.speechInput()
            print(f"< {speech}")
            self.pausable = True
            
            print(self.game.createDetectiveResponse())
            
        self.ended = False
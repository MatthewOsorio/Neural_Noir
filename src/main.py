from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectFrame, DirectButton, DGG
from panda3d.core import TextNode
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import *
from direct.gui.OnscreenText import OnscreenText
import GameController as gc
from NLPSystem.NLPController import NLPController as nlp
from NLPSystem.IntimidatingStyle import IntimidatingSytle
from TTSSystem.TextToSpeechController import TextToSpeechController as ttsc
from SRSystem.SpeechToText import SpeechToText as stt
from DatabaseController import DatabaseController as db
import threading
import time

from ui.menu import menuManager
from ui.interrogationRoom import InterrogationRoom

class main(ShowBase):
    def __init__(self):
        super().__init__()

        self.menuManager = menuManager(self)
        self.interrogationRoom = InterrogationRoom(self)

        self.taskMgr.add(self.checkForGameStart, "Check for Game Start")

        intimidating = IntimidatingSytle()
        nlpController = nlp(intimidating)
        self.game = gc.GameController(stt(), nlpController, ttsc(), db())
        self.mlThreadRun = threading.Thread(target = self.runInterrogation)
        self.roomLoaded = False

    #Will not load the interrogation room until the game actually starts 
    #Note: Give it about a second after "start" is selected for the room to load        
    def checkForGameStart(self, task):
        if self.menuManager.gameStart == True:
            print("Main - True")
            self.interrogationRoom.cameraSetUp()
            self.interrogationRoom.loadModels()    
            self.roomLoaded = True   
            print ("Check - Loaded")
        
            self.mlThreadRun.start()
            return task.done

        return task.cont
   
    def runInterrogation(self):
        print("Run-True")
        self.game.startInterrogation()
        
        while True:
            speech = self.game.speechInput()
            print(f"< {speech}")
            print(self.game.createDetectiveResponse())


app = main()
app.run()
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
    def __init__(self, base):
        self.base = base
        self.room = self.base.loader.loadModel("../blender/converted_room_whole/room.bam")
        self.room.reparentTo(self.base.render)
        self.room.setScale(1)
        self.room.setPos(5.6, 6, 0.2)
        self.room.setHpr(0, 0, 0)
        self.base.disableMouse()
        self.gameState= 'gameplay'

        self.initialStyle = IntimidatingSytle()
        self.nlpController = nlp(self.initialStyle)
        self.game = gc.GameController(stt(), self.nlpController, ttsc(), db())

        #Matt wrote lines 19 - 33
        #Create pause menu but hide it initially
        self.pauseMenu = PauseMenu(self)
        self.pauseMenu.hide()
        self.pauseMenu.hideImage()

        #pause game if escape is pressed
        self.base.accept('escape', self.pauseGame)

    def pauseGame(self):
        if(self.gameState == 'gameplay'):
            self.pauseMenu.show()
            self.pauseMenu.showImage()
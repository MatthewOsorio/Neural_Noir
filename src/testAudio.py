from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectFrame, DirectButton, DGG
from panda3d.core import TextNode
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import *
from direct.gui.OnscreenText import OnscreenText
import threading

import time

from ui.menu import menuManager
from ui.interrogationRoom import InterrogationRoom
from audio import audioManager

class main(ShowBase):
    def __init__(self):
        super().__init__()

        # self.menuManager = menuManager(self)
        # self.interrogationRoom = InterrogationRoom(self)
        self.audioManager = audioManager(self)

        # audInList = self.audioManager.listAudioInput()
        # print(audInList)
        # self.audioManager.selectAudioInput()

        # audOutList = self.audioManager.listAudioOutput()
        # print(audOutList)
        # self.audioManager.selectAudioOutput()

        self.audioManager.testAudioInput()


        # self.taskMgr.add(self.checkForGameStart, "Check for Game Start")
        # self.roomLoaded = False

        # #Stars interrogation api calls on a separate thread once the game is started
        # self.interrogationThread = threading.Thread(target=self.interrogationRoom.runInterrogation)

    # #Will not load the interrogation room until the game actually starts 
    # #Note: Give it about a second after "start" is selected for the room to load        
    # def checkForGameStart(self, task):
    #     if self.menuManager.gameStart == True:
    #         print("Main - True")
    #         self.interrogationRoom.cameraSetUp()
    #         self.interrogationRoom.loadModels()    
    #         self.roomLoaded = True   
    #         print ("Check - Loaded")
        
    #         self.interrogationThread.start()
    #         return task.done

    #     return task.cont

app = main()
app.run()
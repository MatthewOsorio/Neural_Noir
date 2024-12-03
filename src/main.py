from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectFrame, DirectButton, DGG
from panda3d.core import TextNode
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import *
from direct.gui.OnscreenText import OnscreenText
from direct.stdpy.threading import BoundedSemaphore, Condition, Event, ExternalThread, Lock, MainThread, RLock, Semaphore, Thread, ThreadBase, Timer, active_count, current_thread, enumerate, main_thread, setprofile, settrace, stack_size


import time

from ui.menu import menuManager
from ui.interrogationRoom import InterrogationRoom
from connection_utils import Connection
from ui.connectionDisplay import ConnectionDisplay

class main(ShowBase):
    def __init__(self):
        super().__init__()

        self.start = False
        self.menuManager = menuManager(self, self.start)
        self.interrogationRoom = None

        self.taskMgr.add(self.checkForGameStart, "Check for Game Start")
        
        self.roomLoaded = False
   
    def checkGameStartFlag(self):
        self.taskMgr.add(self.checkForGameStart, "Check for Game Start")

    #Will not load the interrogation room until the game actually starts 
    #Note: Give it about a second after "start" is selected for the room to load        
    def checkForGameStart(self, task):
        if self.menuManager.gameStart == True:
            self.interrogationRoom = InterrogationRoom(self, self.menuManager)
            #print("Main - True")
            self.interrogationRoom.cameraSetUp()
            self.interrogationRoom.loadModels()    
            self.roomLoaded = True   
            #Stars interrogation api calls on a separate thread once the game is started
            self.interrogationThread = Thread(target=self.interrogationRoom.runInterrogation)
            self.interrogationThread.start()
            self.interrogationRoom = None
            return task.done

        return task.cont
    
app = main()
app.run()
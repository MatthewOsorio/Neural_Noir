from backend.BackendInterface.GameManager import GameManager

from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectFrame, DirectButton, DGG
from panda3d.core import TextNode
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import *
from direct.gui.OnscreenText import OnscreenText
#from direct.stdpy.threading import BoundedSemaphore, Condition, Event, ExternalThread, Lock, MainThread, RLock, Semaphore, Thread, ThreadBase, Timer, active_count, current_thread, enumerate, main_thread, setprofile, settrace, stack_size
import sys
#from direct.stdpy.threading import Thread
import time

from frontend.ui.menu.menu import menuManager
from frontend.ui.interrogationRoom import InterrogationRoom
from frontend.ui.connection_utils import Connection
from frontend.ui.connectionDisplay import ConnectionDisplay

import threading

class main(ShowBase):
    def __init__(self):
        super().__init__()

        self.start = False
        self.menuManager = menuManager(self, self.start)
        self.interrogationRoom = None

        self.taskMgr.add(self.checkForGameStart, "Check for Game Start")
        self.roomLoaded = False

        self.connection = None
        self.connectionDisplay = None
        self.connections()

        self.voiceVolume = 1
        self.sfxVolume = 1
        self.threadEvent = threading.Event()
        self.interrogationThread = None
   
    def checkGameStartFlag(self):
        self.taskMgr.add(self.checkForGameStart, "Check for Game Start")

    #Will not load the interrogation room until the game actually starts 
    #Note: Give it about a second after "start" is selected for the room to load        
    def checkForGameStart(self, task):
        self.connections()
        def on_success():
            self.connectionDisplay.destroyConnectionStatus()
            
            self.interrogationRoom = InterrogationRoom(self, self.menuManager)
            #print("Main - True")
            self.interrogationRoom.cameraSetUp()
            self.interrogationRoom.loadModels()
            self.interrogationRoom.loadLighting()
            self.roomLoaded = True   
            self.interrogationRoom.game.begin = True
            #Stars interrogation api calls on a separate thread once the game is started
            self.interrogationThread = threading.Thread(target=(self.interrogationRoom.beginInterrogation), daemon = True)
            self.interrogationThread.start()

        if self.menuManager.gameStart == True:
            self.connectionDisplay.checkInternetAndDisplay(
                on_success=on_success,
                on_failure=sys.exit
            )
            return task.done
        
        return task.cont
    
    def returnToMenu(self, task=None):

        self.connectionDisplay.destroyConnectionStatus()
        self.interrogationRoom = None
        self.interrogationThread = None
        self.menuManager.showMain()
        self.menuManager.showImage()
        if task:
            return task.done
        
    def connections(self):
        self.connection = Connection()
        self.connectionDisplay = ConnectionDisplay(self, self.connection)

    def cleanUpThreads(self):
        self.threadEvent.set()
        print("Initial thread clean up function")
        if self.interrogationThread is not None:
            print("Joining initial thread")
            self.interrogationThread.join(timeout = 2)
        
app = main()
app.run()
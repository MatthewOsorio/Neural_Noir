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
from frontend.ui.tutorialRoom import TutorialRoom
from frontend.ui.warnings.dataUsageWarning import Warning

from panda3d.core import MovieTexture, CardMaker, TextureStage
import os
from panda3d.core import Filename
current_dir = os.path.dirname(os.path.abspath(__file__))
video = os.path.join(current_dir, "..", "Assets", "Video", "video_intro.mp4")
video = os.path.normpath(video)
video = Filename.fromOsSpecific(video).getFullpath()

import threading

class main(ShowBase):
    def __init__(self):
        super().__init__()
        self.base = ShowBase
        self.interrogationRoom = None
        self.start = False
        self.movie = None
        self.card = None
        self.skipMovie = False
        self.warning = Warning(self)
        self.warning.show()
        self.warning.button['command'] = self.continueSetUp

    def continueSetUp(self):
        self.warning.hide()
        self.menuManager = menuManager(self, self.start)

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
            
            #Slight delay so that video doesn't play before the connection screen disappears
            taskMgr.doMethodLater(0.5, self.playMovie, "movieTask1")

            #Kept this here so that models and all that could load during the video but if you want to load it after the video for things like animations
            #Move whatever you need to "StartAfterMovie" method
            self.interrogationRoom = InterrogationRoom(self, self.menuManager)
            #print("Main - True")
            self.interrogationRoom.cameraSetUp()
            self.interrogationRoom.loadModels()
            self.interrogationRoom.loadLighting()


        def on_successTutorial():
            self.connectionDisplay.destroyConnectionStatus()
            
            self.interrogationRoom = TutorialRoom(self, self.menuManager)
            #print("Main - True")
            self.interrogationRoom.cameraSetUp()
            self.interrogationRoom.loadModels()
            self.interrogationRoom.loadLighting()
            self.roomLoaded = True   
            self.interrogationRoom.game.begin = True
            #Stars interrogation api calls on a separate thread once the game is started
            self.interrogationThread = threading.Thread(target=(self.interrogationRoom.beginInterrogation), daemon = True)
            self.interrogationThread.start()

        if self.menuManager.gameStart == True and self.menuManager.tutorialStart == False:
            self.connectionDisplay.checkInternetAndDisplay(
                on_success=on_success,
                on_failure=sys.exit
            )
            return task.done
     
        if self.menuManager.tutorialStart == True and self.menuManager.gameStart == False:
            self.connectionDisplay.checkInternetAndDisplay(
                on_success=on_successTutorial,
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

    def playMovie(self, task):
        #print("Play movie")
        self.movie = MovieTexture("name")
        v = self.movie.read(video)
        self.movie.setLoop(False)
        self.movie.play()

        hSize = self.getAspectRatio()

        cm = CardMaker("movieCard")
        cm.setFrame(-1.315*hSize, 1.315*hSize, -1, 1)
        self.card = aspect2d.attachNewNode(cm.generate())
        self.card.setTexture(self.movie)
        self.card.setBin('fixed', 1)

        self.card.setTexScale(TextureStage.getDefault(), self.movie.getTexScale()[0], self.movie.getTexScale()[1])
        self.card.setTexOffset(TextureStage.getDefault(), 0, 0)

        self.skipButton()

        taskMgr.add(self.checkEndOfMovie, "movieTask")
        return task.done

    def checkEndOfMovie(self, task): 
        #print("Check for end of movie")
        if self.movie.getTime() >= self.movie.getVideoLength() or self.skipMovie is True:
            self.card.removeNode()  
            self.startAfterMovie()
            #print("Ending movie")
            return task.done
        return task.cont

    def startAfterMovie(self):
        taskMgr.remove("movieTask")
        taskMgr.remove("movieTask1")
        self.button.hide()
        self.skipMovie = False
        self.roomLoaded = True   
        self.interrogationRoom.game.begin = True
        self.interrogationThread = threading.Thread(target=(self.interrogationRoom.beginInterrogation), daemon = True)
        print("Start thread")
        self.interrogationThread.start()

    def skipButton(self):
        #I put the button on the left for now so it doesn't cover the sora logo
        self.button = DirectButton(
            text = "Skip",
            command = self.setSkipMovie,
            sortOrder = 1,
            text_font = self.menuManager.font,
            text_fg = (1, 1, 1, 1),
            frameColor = (0, 0, 0, 0.8),
            pos = (-1.7, -0.9, -0.9),
            scale = 0.1
        )

        self.button.show()

        self.button.bind(DGG.ENTER, lambda event: self.menuManager.setColorHover(self.button))  
        self.button.bind(DGG.EXIT, lambda event: self.menuManager.setColorDefault(self.button)) 

    def setSkipMovie(self):
        self.skipMovie = True

app = main()
app.run()
from frontend.ui.menu.PauseMenu import PauseMenu
from backend.BackendInterface.GameManager import GameManager
from frontend.ui.overlay.Overlay import Overlay
from frontend.stages.state1 import State1
from frontend.stages.state2 import State2
from direct.task import Task
from direct.task.TaskManagerGlobal import taskMgr 
import threading

from panda3d.core import *
import time

import os
from panda3d.core import Filename
current_dir = os.path.dirname(os.path.abspath(__file__))
prompt = os.path.join(current_dir, "..", "..", "..", "Assets", "Images", "introPrompt.png")
prompt = os.path.normpath(prompt)
prompt = Filename.fromOsSpecific(prompt).getFullpath()

#Code originally written by Christine 
#Modified by Evie 
class InterrogationRoom:
    def __init__(self, base, menu):
        self.base = base
        self.menu = menu

        self.useEmotibit = True

        self.base.disableMouse()
        self.gameState= 'gameplay'

        #pause game if escape is pressed
        self.base.accept('escape', self.pauseGame)

        self.game = GameManager()  
        self.game.setupGame(self.useEmotibit)
        self.game.setUseEmotibit(self.useEmotibit)

        #Matt wrote lines 19 - 33
        #Create pause menu but hide it initially
        self.menu.initializePauseMenu()
        self.menu.pauseMenu.getGame(self.game)
        self.menu.pauseMenu.getRoom(self)
        self.menu.pauseMenu.hide()
        self.menu.pauseMenu.hideImage()

        self.Overlay = Overlay(self)      
        self.Overlay.show()
        
        #Game will not be pausable if it is the user's turn to reply
        self.pausable = False

        self.current = None

        self.prompt = prompt

        self.thread = None
        
    def pauseGame(self):
        #Requires the game to not be paused, not be on a menu, and not be the player's turn to reply 
        if(self.gameState == 'gameplay' and self.menu.gameState == 'gameplay' and self.pausable == True):
            self.menu.pauseMenu.show()
            self.menu.pauseMenu.showImage()
            self.gameState = 'paused'
            self.game._tts.audio.pauseSpeech()
            self.Overlay.hide()
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

        # load policeman
        self.policeman = self.base.loader.loadModel("../blender/policeman/converted/policeman_converted.bam")
        self.policeman.setScale(0.5)
        self.policeman.setPos(-0.43, 2, -1.5)
        self.room.setHpr(0, 0, 0)
        self.policeman.reparentTo(self.base.render)
        
    def unloadModels(self):
        self.room.detachNode()
        self.room.removeNode()
        self.room = None

        self.policeman.detachNode()
        self.policeman.removeNode()
        self.policeman = None
        #print("Unload models")

    def loadLighting(self):
        # Point lighting
        # self.plight = PointLight('plight')
        # self.plight.setColor((0.5,0.5,0.5,1))
        # self.plnp = self.base.render.attachNewNode(self.plight)
        # self.plnp.setPos(0,2,3)
        # self.base.render.setLight(self.plnp)

        # Ambient lighting
        self.ambient = AmbientLight('ambient')
        self.ambient.setColor((0.3, 0.3, 0.3, 1))
        self.ambientNP = self.base.render.attachNewNode(self.ambient)
        self.base.render.setLight(self.ambientNP)

   #Run on separate thread

    def beginInterrogation(self):
        self.pausable = True
        self.ended = False
        
        self.Overlay.flashback.setImage(self.prompt)
        self.Overlay.flashback.show()

        flashback = self.Overlay.flashback.getActive()
        while flashback == True:
            flashback = self.Overlay.flashback.getActive()
              
        if self.useEmotibit == True:
            self.Overlay.showBioData()
        
        self.testStates = [State1(), State2()]

        self.state = self.testStates[0]
    
        self.state.setGame(self.game)

        self.state.testPrint()

        response = self.state.begin()
        self.state.convert()
        self.current = 0
        self.Overlay.ptt.showPTTButton()
        #Get the speech input
        taskMgr.add(self.speechUI, "UpdateSpeechTask")
        
       
    #Updates the overlay to show the PTT Button
    def speechUI(self, task):
        
        pttActive = self.Overlay.ptt.getPTTActive()
        if pttActive == False: 
            self.Overlay.ptt.hidePTTButton()
            print("talk")
            self.thread = threading.Thread(target=self.processSpeech, daemon=True)
            self.thread.start()
            return task.done 

        return task.cont
     
    #Speech input part 
    def processSpeech(self):
        self.pausible = False
        self.Overlay.hideSubtitlesBox()
        speech = self.game.listenToUser()
        self.game.insertInteractionInDB()

        taskMgr.add(lambda task: self.speechUIPost(speech, task), "UpdateSpeechTask2")

    def speechUIPost(self, speech, task):

        self.Overlay.ptt.hidePTTButton()
     
        print(f"{speech}")
        #Get the response
        self.thread = threading.Thread(target=self.processResponse, daemon=True)
        self.thread.start()
        return task.done
              
    #Response processing part
    def processResponse(self):
        self.pausable = True
        
        response = self.state.generateResponse()

        if response != False:
            #Update the overlay to show the response
            taskMgr.add(lambda task: self.responseUI(response, task), "UpdateResponseTask")
            
        else:
            self.current = self.current + 1
            print(f"State {self.current}")
            self.state = self.testStates[self.current]

            self.state.setGame(self.game)
            response = self.state.begin()
            print("New state response")
            taskMgr.add(lambda task: self.responseUI(response, task), "UpdateResponseTask")

            print("End")

    #Updates subtitles if applicable
    def responseUI(self, response, task):
        print(response)
        if (self.menu.subtitles == True):
            self.Overlay.subtitles.setResponse(response)
            self.Overlay.subtitles.updateSubtitles()
            self.Overlay.showSubtitlesBox()
        
        #Convert the response to speech
        self.thread = threading.Thread(target=self.responseToSpeech, daemon=True)
        self.thread.start()
        return task.done

    #TTS process
    def responseToSpeech(self):
        self.state.convert()
        
        #Hide the subtitles
        taskMgr.add(self.updateResponse, "Update")
    
    #Hides subtitles
    def updateResponse(self, task):
        self.Overlay.hideSubtitlesBox()

        #If the game has not been quit, restart the process
        if self.ended == False:
            self.Overlay.ptt.showPTTButton()
            #threading.Thread(target=self.processSpeech, daemon=True).start()
            self.processNext()
            return task.done
    
    def processNext(self):
        self.Overlay.ptt.showPTTButton()
        taskMgr.add(self.speechUI, "Update")
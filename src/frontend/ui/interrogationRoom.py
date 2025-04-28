from frontend.ui.menu.PauseMenu import PauseMenu
from frontend.ui.animations import Animations
from backend.BackendInterface.GameManager import GameManager
from frontend.ui.overlay.Overlay import Overlay
from frontend.stages.state1 import State1
from frontend.stages.state2 import State2
from frontend.stages.state3 import State3
from frontend.stages.state4 import State4
from direct.actor.Actor import Actor
from direct.task import Task
from direct.task.TaskManagerGlobal import taskMgr
import threading

from panda3d.core import *

import os
from panda3d.core import Filename
current_dir = os.path.dirname(os.path.abspath(__file__))
prompt = os.path.join(current_dir, "..", "..", "..", "Assets", "Images", "introPromptTest.png")
prompt = os.path.normpath(prompt)
prompt = Filename.fromOsSpecific(prompt).getFullpath()

#Code originally written by Christine 
#Modified by Evie 
class InterrogationRoom:
    def __init__(self, base, menu):
        self.base = base
        self.menu = menu

        self.useEmotibit = self.menu.settingsMenu.getUseEmotibit()
        self.difficulty = self.menu.settingsMenu.getDifficulty()

        self.base.disableMouse()
        self.base.camLens.setNear(0.01)
        self.gameState= 'gameplay'

        #pause game if escape is pressed
        self.base.accept('escape', self.pauseGame)

        self.voiceVolume = self.base.voiceVolume
        self.sfxVolume = self.base.sfxVolume

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

        self.animation = Animations(self.base)
        
        self.Overlay = Overlay(self)      
        self.Overlay.show()
        
        #Game will not be pausable if it is the user's turn to reply
        self.pausable = False

        self.current = 0

        self.prompt = prompt

        self.threadEvent = threading.Event()

        self.thread = None

        self.redoable = False

        self.testStates = None

        self.currentLine = 0
        
        self.currentEvidence = None
        
    def pauseGame(self):
        #Requires the game to not be paused, not be on a menu, and not be the player's turn to reply 
        if(self.gameState == 'gameplay' and self.menu.gameState == 'gameplay' and self.pausable == True and not self.Overlay.connectionError):
            self.menu.pauseMenu.show()
            self.menu.pauseMenu.showImage()
            self.gameState = 'paused'
            self.game._tts.audio.pauseSpeech()
            self.Overlay.hide()
        if(self.gameState == 'gameplay' and self.menu.gameState == 'gameplay' and self.pausable == False):
            self.base.menuManager.audio.playSound("errorSound")
        
    def cameraSetUp(self):
        #Moved the camera back slightly so that it does not clip the table
        self.base.camera.setPos(0, -0.18 , 0)
        #Test print for the camera position if we need to change it
        print(self.base.camera.getPos())

        self.cameraSensitivity = 10
        self.horizontal = 0
        self.vertical = 0

        #Updates the camera angle
        self.base.taskMgr.add(self.moveCamera, "Move Camera")

        ##################################################
        # # CAMERA AT LEFT SIDE FACING MILLER
        # self.base.camera.setPos(-3, 1, -0.1)
        # self.base.camera.setHpr(295, -5, 0)

        # # CAMERA AT RIGHT SIDE OF ROOM FACING HARRIS
        # self.base.camera.setPos(2.75, 1, -0.5)
        # self.base.camera.setHpr(70, 4, 1)
        
        # self.cameraSensitivity = 10
        # self.horizontal = 0
        # self.vertical = 0
        ##################################################
        
    #Allows users to rotate the camera slightly to "look around"
    def moveCamera(self, base):
        if self.base.mouseWatcherNode.hasMouse():
            self.x = self.base.mouseWatcherNode.getMouseX()
            self.y = self.base.mouseWatcherNode.getMouseY()

            #X value multiplied by -1 so that the horizontal camera movement is not inverted
            self.horizontal = (self.x * self.cameraSensitivity) * -1
            self.vertical = self.y * self.cameraSensitivity

            clamped_horizontal = max(min(self.horizontal, 60), -60)  # Left/right limit
            clamped_vertical = max(min(self.vertical, 60), -0.8)      # Up/down limit

            self.base.camera.setHpr(clamped_horizontal, clamped_vertical, 0)

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

        # Play animations based on sentiment keyword
        self.sentimentToAnimation = {
            "Harris": {
                "neutral": self.animation.playHarrisIdle,
                "aggressive": self.animation.playHarrisBang,
                "mocking": self.animation.playHarrisLaugh,
                "skeptical": self.animation.playHarrisLean,
                "dismissive": self.animation.playHarrisLean,
                "incredulous": self.animation.playHarrisLaugh,
                "accusatory": self.animation.playHarrisIdle
            },
            "Miller": {
                "neutral": self.animation.playMillerIdle,
                "sympathetic": self.animation.playMillerTalk,
                "serious": self.animation.playMillerIdle,
                "concerned": self.animation.playMillerLean,
                "reassuring": self.animation.playMillerTalk,
                "disappointed": self.animation.playMillerLean,
                "accusatory": self.animation.playMillerIdle
            }
        }
        
        self.loadAndStopAnimations()

        # Test Animations class
        # self.animation.playHarrisIdle()
        # self.animation.playMillerIdle()

    #Pre load all animations and stop them to prevent thread blocking later
    def loadAndStopAnimations(self):
        for speaker, animations in self.sentimentToAnimation.items():
            for sentiment, playAnimation in animations.items():
                playAnimation()

        self.animation.harris.stop()
        self.animation.miller.stop()        

    def unloadModels(self):
        self.room.detachNode()
        self.room.removeNode()
        self.room = None

        self.animation.harris.cleanup()
        self.animation.harris.removeNode()
        self.animation.harris = None

        self.animation.miller.cleanup()
        self.animation.miller.removeNode()
        self.animation.miller = None

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
        self.menu.audioMenu.setVoiceVolumeSlider(self.voiceVolume)
        self.menu.audioMenu.setSFXVolumeSlider(self.sfxVolume)

        self.pausable = False
        self.ended = False
        self.current = 0
        self.Overlay.flashback.setImage(self.prompt)
        self.Overlay.flashback.show()

        flashback = self.Overlay.flashback.getActive()
        while flashback == True:
            flashback = self.Overlay.flashback.getActive()
              
        if self.useEmotibit == True:
            self.game._bioController.incrementError = True
            self.Overlay.startEmotiBitCheck()
            self.Overlay.showBioData()
        
        self.testStates = [State1(), State2(), State3(), State4()]

        self.state = self.testStates[0]
    
        self.state.setGame(self.game)

        self.state.testPrint()

        response = self.state.begin()
        self.currentLine = 0
        taskMgr.add(lambda task: self.responseUI(task), "UpdateResponseTask")
        self.state.convert()
        #self.Overlay.ptt.showPTTButton()
       # self.redoable = True
        #Get the speech input
        #taskMgr.add(self.speechUI, "UpdateSpeechTask")
  

    #Updates the overlay to show the PTT Button
    def speechUI(self, task):
        self.pausable = True
        pttActive = self.Overlay.ptt.getPTTActive()
        if pttActive == False: 
            self.pausable = False
            self.Overlay.ptt.hidePTTButton()
            print("talk")
            self.thread = threading.Thread(target=self.processSpeech, daemon=True)
            if self.threadEvent.is_set() == False:
                self.thread.start()
            return task.done 

        return task.cont
     
    #Speech input part 
    def processSpeech(self):
        
        self.Overlay.hideSubtitlesBox()
        speech = self.game.listenToUser()
        
        self.Overlay.userSpeech.active = True
        self.Overlay.userSpeech.redo = False

        taskMgr.add(lambda task: self.speechUIPost(speech, task), "UpdateSpeechTask2")

    def speechUIPost(self, speech, task):

        self.Overlay.ptt.hidePTTButton()
     
        #print(f"{speech}")
        #Get the response
        self.Overlay.userSpeech.setSpeech(speech)
        self.Overlay.showUserInputBox()

        if self.redoable is True:
            self.Overlay.acceptSpeechButton.show()
            self.Overlay.redoSpeechButton.show()
            
        elif self.redoable is False:
            self.Overlay.redoSpeechButton.hide()

        userInputActive = self.Overlay.userSpeech.getActive()
        if userInputActive == False and self.Overlay.userSpeech.redo == False:
            self.Overlay.hideUserInputBox()
            self.game.insertInteractionInDB(speech, "Player")
            self.thread = threading.Thread(target=self.processResponse, daemon=True)
            if self.threadEvent.is_set() == False:
                self.thread.start()
            return task.done
        elif self.redoable == True and userInputActive == False and self.Overlay.userSpeech.redo == True:
            self.redoable = False
            self.Overlay.hideUserInputBox()
            self.Overlay.ptt.showPTTButton()
            taskMgr.add(self.speechUI, "UpdateSpeechTask")
            self.pausable = True
            return task.done
        
        return task.cont
              
    #Response processing part
    def processResponse(self):
        self.game.sendUserResponseToAI()

        response = self.state.generateResponse()

        if response != False:
            #Update the overlay to show the response
            #taskMgr.add(lambda task: self.responseUI(response, task), "UpdateResponseTask")
            #print(f"Current Evidence: {self.game._aiController.getCurrentEvidence()}")
            #self.currentEvidence = self.game._aiController.getCurrentEvidence()
            self.currentLine = 0
            taskMgr.add(lambda task: self.responseUI(task), "UpdateResponseTask")
            
        else:
            taskMgr.doMethodLater(1.0, self.startNextStateTask, "StartNextTask")

    def startNextStateTask(self, task):
        self.current = self.current + 1
        print(f"State {self.current}")
        self.state = self.testStates[self.current]

        self.state.setGame(self.game)
        self.state.setOverlay(self.Overlay)
        self.state.setUseEmotibit(self.useEmotibit)
        self.thread = threading.Thread(target = self.beginNextState, daemon = True)
        if self.threadEvent.is_set() is False:
            self.thread.start()
        return task.done

    def beginNextState(self):
        response = self.state.begin()
        #print(f"Current Evidence: {self.game._aiController.getCurrentEvidence()}")
        #self.currentEvidence = self.game._aiController.getCurrentEvidence()
        print("New state response")
        self.currentLine = 0
        taskMgr.add(lambda task: self.responseUI(task), "UpdateResponseTask")

        print("End")                           

    # Updates subtitles if applicable
    # Also gets sentiment for each animation prior to playing the next response
    def responseUI(self, task):
        count = self.currentLine
        #print(f"Response: {response}")
        if (self.menu.subtitles == True):
            subtitlesString = f"{self.state.speakers[count]}: {self.state.texts[count]}"
            print(f"Sub string {count}: {subtitlesString}")
            self.Overlay.subtitles.setResponse(subtitlesString)
            self.Overlay.subtitles.updateSubtitles()
            self.Overlay.showSubtitlesBox()

        #Probably put detective animation call here 
        #self.animationTest(speakers[count], sentiment[count])
        self.game.insertInteractionInDB(self.state.texts[count], self.state.speakers[count])

        # Get speaker and sentiment for animation
        speaker = self.state.speakers[count]
        sentiment = self.state.sentiments[count]

        # Play animation based on sentiment
        if speaker in self.sentimentToAnimation and sentiment in self.sentimentToAnimation[speaker]:
            print(f"Playing {speaker}'s animation for sentiment: {sentiment}")
            self.sentimentToAnimation[speaker][sentiment]()


        print (f"Audio Path {count}: {self.state.audioFilePaths[count]}")
        #self.game._tts.speak(self.state.audioFilePaths[count])
        self.thread = threading.Thread(target=self.playAudio, args=(self.state.audioFilePaths[count],), daemon=True)
        if self.threadEvent.is_set() == False:
            self.thread.start()

        return task.done
    
    def playAudio(self, audioPath):
        self.game._tts.speak(audioPath)

        if self.currentLine < len(self.state.audioFilePaths) - 1:
            self.currentLine = self.currentLine + 1
            taskMgr.add(lambda task: self.responseUI(task), "UpdateResponseTask")
        else:
            self.state.resetResponse()
            taskMgr.add(self.updateResponse, "Update")

    #Hides subtitles
    def updateResponse(self, task):
        self.Overlay.hideSubtitlesBox()

        if self.current > 0 and len(self.state.introduce) > 0:
            if self.state.introduce[0] is True:
                self.Overlay.hideBioData()
                print(f"Introduce true - {self.state.introduce}")
                print(f"Current photo: {self.state.photos[0]}")
                self.Overlay.evidence.setImage(self.state.photos[0])
                self.Overlay.evidence.show()
                self.Overlay.evidence.button["command"] = self.evidenceImageCallback
            else:
                taskMgr.add(self.processAfterEvidenceImage, "afterImageTask")
        else:
            taskMgr.add(self.processAfterEvidenceImage, "afterImageTask")
        return task.done
    
    
    def evidenceImageCallback(self):
        self.Overlay.evidence.hide()
        if self.current > 0:
            self.state.resetPhotos()
        taskMgr.add(self.processAfterEvidenceImage, "afterImageTask")

    def processAfterEvidenceImage(self, task):
        #If the game has not been quit, restart the process
        if self.useEmotibit is True:
            self.Overlay.showBioData()
            
        if self.ended == False and not self.Overlay.connectionError:
            self.Overlay.ptt.showPTTButton()
            #threading.Thread(target=self.processSpeech, daemon=True).start()
            self.processNext()
            return task.done
    
    def processNext(self):
        self.Overlay.ptt.showPTTButton()
        self.redoable = True
        taskMgr.add(self.speechUI, "UpdateSpeech")

    def cleanUpTasks(self):
        taskMgr.remove("Update")
        taskMgr.remove("UpdateResponseTask")
        taskMgr.remove("UpdateSpeech")
        taskMgr.remove("UpdateSpeechTask")
        taskMgr.remove("UpdateSpeechTask2")
        self.Overlay.cleanUpTasks()

    def cleanUpThreads(self):
        self.threadEvent.set()
        if self.thread is not None and self.thread.is_alive():
            print("Joining game thread")
            self.thread.join(timeout = 2)

        if self.useEmotibit == True:
            self.game._bioController.cleanThread()

        self.Overlay.cleanUpThreads()
        self.base.cleanUpThreads()
        


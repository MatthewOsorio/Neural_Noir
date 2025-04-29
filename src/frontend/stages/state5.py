from backend.BackendInterface.GameManager import GameManager
from backend.StoryGraph.EndGame import EndGame
from backend.TTSSystem.TextToSpeechController import TextToSpeechController
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectFrame, DirectButton, DGG
from panda3d.core import TextNode
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from direct.gui.DirectScrolledFrame import DirectScrolledFrame
import json
from panda3d.core import TransparencyAttrib

class State5:
    def __init__(self):
        self.game = None
        self.state = None
        self.endPhase = False
        self.verdict = None
        self.overlay = None
        self.useEmotbit = None
        self.verdictsList = []
        self.ttsController = TextToSpeechController()
        self.endgame = None

    def setGame(self, game):
        self.game = game

    def setUseEmotibit(self, useEmotibit):
        self.useEmotibit = useEmotibit

    def setOverlay(self, overlay):
        self.overlay = overlay

    def begin(self):
        self.game._gameState.updateState(5)

        self.endgame = EndGame(self.game._aiController._storyGraph, self.overlay.base.difficulty)
        self.endPhase = self.overlay.base.ended = True
        millerFinalLine = [{"Speaker": "Detective Miller", "Text": "Alright, we're done here."}]
        self.ttsController.generateTTS(millerFinalLine)
        taskMgr.add(lambda task: self.waitForAudio(millerFinalLine[0], task), "waitTask")


    def waitForAudio(self, line, task):
        if "AudioFilepath" not in line:
            return task.again
        elif("AudioFilepath" in line):
            self.continueEnd(line)
            return task.done
        
    def continueEnd(self, line):
        self.ttsController.speak(line["AudioFilepath"])



        self.verdict = self.endgame.determineEnding()
        self.verdict = self.endgame.determineEnding()
        

        if self.overlay is not None:
            self.endingScreen()

    def endingScreen(self):
        print("Show ending screen")

        self.endFrame = DirectFrame(
        frameColor=(0, 0, 0, 1),
        frameSize=(-1, 1, -1, 1),
        parent = self.overlay.base.base.aspect2d
        )

        self.endBackground = OnscreenImage(
            self.overlay.base.base.menuManager.backGroundBlack,
            parent=self.endFrame,
            scale=(3),
            pos=(0 , 0, 0),
        )

        self.verdictText = OnscreenText(
            parent = self.endFrame,
            text = "Verdict",
            fg = (1, 1, 1, 1),
            scale = 0.25,
            pos = (0, 0.7, 0.7),
            font = self.overlay.base.menu.font
        )

        self.endFrame.setTransparency(TransparencyAttrib.MAlpha)
        self.endFrame.setAlphaScale(0)

        self.endFrame.show()

        verdicts = self.getVerdicts()

        for verdict in verdicts:
            verdictStr = f"{verdict[0]} : {verdict[1]}"
            self.verdictsList.append(verdictStr)
            
        print(self.verdictsList)

        verdictCount = len(self.verdictsList)
        spacing = 0.15  # vertical space for each line
        height = verdictCount * spacing

        self.scrollableFrame = DirectScrolledFrame(
            parent= self.endFrame,
            frameSize= (-1.5, 1.5, -0.70, 0.70),
            frameColor= (0, 0, 0, 0),
            pos= (0, 0, 0),
            scrollBarWidth= 0.05,
            canvasSize=(-1.5, 1.5, -0.8 , 0.1)    ,
            horizontalScroll_decButton_relief=None,
            horizontalScroll_incButton_relief=None,
            horizontalScroll_frameSize=(0, 0, 0, 0),
            sortOrder = 2
            )
        
        textYPos = 0
        for text in self.verdictsList:
            DirectLabel(
                parent= self.scrollableFrame.getCanvas(),
                text= text,
                text_align= TextNode.ALeft,
                text_scale= 0.05,
                pos=(-1.4, 0, textYPos),
                frameColor=(0, 0, 0, 0),
                text_fg=(1, 1, 1, 1),
                text_wordwrap= 55
            )
            textYPos -= spacing
        
        self.button = DirectButton(
            text = "Finish",
            command = self.returnToMain,
            sortOrder = 1,
            text_font = self.overlay.base.menu.font,
            text_fg = (1, 1, 1, 1),
            frameColor = (0, 0, 0, 0.8),
            pos = (1.7, -0.9, -0.9),
            scale = 0.1,
            parent = self.endFrame
        )

        self.button.bind(DGG.ENTER, lambda event: self.overlay.base.menu.setColorHover(self.button))  
        self.button.bind(DGG.EXIT, lambda event: self.overlay.base.menu.setColorDefault(self.button)) 

        self.fadeInEndingScreen()
        self.displayEndingScreen()

    def fadeInEndingScreen(self):
         fade = LerpFunc(
             self.endFrame.setAlphaScale,
             fromData=0,
             toData=1,
             duration=2.0,
         )
         fade.start()

    def displayEndingScreen(self):

        if self.verdict == "GUILTY":
            # call method to pull up Guilty ending screen and monologue
            #test
            print("YOU HAVE BEEN PROVEN GUILTY")
        elif self.verdict == "NOT GUILTY":
            # call method to pull up Not Guilty ending screen and monologue
            #test
            print("YOU HAVE BEEN PROVEN INNOCENT")
        elif self.verdict == "INCONCLUSIVE":
            # call method to pull up Inconclusive ending screen and monologue
            print("THE INTERROGATION HAS FAILED TO PROVE YOU INNOCENT OR GUILTY")

        vText = str(self.verdict)
        self.verdictText.setText(vText)

    def getVerdicts(self):
        verdicts = self.game.getVerdictsFromDB()
        return verdicts
    
    def returnToMain(self):
        self.endFrame.hide()
        self.overlay.evidenceBox.hide()
        self.overlay.base.menu.pauseMenu.returnToMain()


from backend.BackendInterface.GameManager import GameManager

import os
from panda3d.core import Filename
current_dir = os.path.dirname(os.path.abspath(__file__))
prompt = os.path.join(current_dir, "..", "..", "..", "Assets", "Images", "state2contexttest.png")
prompt = os.path.normpath(prompt)
prompt = Filename.fromOsSpecific(prompt).getFullpath()

#Feel free to change this class as needed. 
class State2:
    def __init__(self):
        self.game = None
        self.state = None
        self.response = None
        self.endPhase = False
        self.overlay = None
        self.image = prompt
        self.useEmotibit = False

        self.speakers = []
        self.texts = []
        self.audioFilePaths = []
        self.sentiments = []

        self.currentEvidence = None

        self.evidenceVerdicts = None


    def testPrint(self):
        print("This is state 2")  
    
    def setGame(self, game):
        self.game = game

    def setUseEmotibit(self, useEmotibit):
        self.useEmotibit = useEmotibit

    def setOverlay(self, overlay):
        self.overlay = overlay

    def begin(self):
        self.game._gameState.updateState(2)

        self.overlay.flashback.setImage(self.image)
        self.overlay.flashback.show()
        self.overlay.hideBioData()

        flashback = self.overlay.flashback.getActive()
        while flashback == True:
            flashback = self.overlay.flashback.getActive()

        self.passToVerdict()

        if self.useEmotibit:
            self.overlay.showBioData()
        
        self.response = self.game.generateAIResponse() 

        print ("State 2 response: ", self.response)
        if self.response is not False:
            self.parseResponse(self.response)        
            self.currentEvidence = self.overlay.base.game._aiController.getCurrentEvidence()
            self.overlay.base.currentEvidence = self.evidenceString()
            self.overlay.evidenceBoxSetText()
            self.overlay.evidenceBoxPopOut() 

        return self.response
        
    def convert(self):
        self.game.convertTTS(self.response)
        pass
    
    def generateResponse(self):
        print("Generating response")
        self.response = self.game.generateAIResponse()

        if self.response == False:
            print("Ending phase")
            self.endPhase = True

        if self.response is not False:
            self.setEvidenceVerdict(None)
            self.parseResponse(self.response)

            self.currentEvidence = self.overlay.base.game._aiController.getCurrentEvidence()
            self.overlay.base.currentEvidence = self.evidenceString()        
            self.overlay.evidenceBoxSetText()
        
        return self.response
    
    def introduceEvidence(self):
        self.game._aiController.introduceEvidence()

    def parseResponse(self, response):

        print (response)

        for line in response:
            speaker = line.get("Speaker")
            text = line.get("Text")
            audioF = line.get("AudioFilepath")
            sentiment = line.get("Sentiment")

            if speaker is not None:
                self.speakers.append(speaker)
            
            if text is not None:
                self.texts.append(text)

            if audioF is not None:
                self.audioFilePaths.append(audioF)

            if sentiment is not None:
                self.sentiments.append(sentiment)
           # print(f"audio path: {line.get('AudioFilepath')}")

        for line in self.speakers:
            print(line)
    
    
    def resetResponse(self):
        self.speakers = []
        self.texts = []
        self.audioFilePaths = []
        self.sentiments = []

    def evidenceString(self):
        evidence = self.currentEvidence.split("–")
        evidenceStr = evidence[0]
        return evidenceStr
    
    def setEvidenceVerdict(self, verdict):
        print("Changing color for verdict")
        if verdict == None:
            self.overlay.evidenceText.fg = (1, 1 , 1, 1)
            print("Verdict is none")
        if verdict == "untruthful":
            self.overlay.evidenceText.fg = (1, 0, 0, 1)
            print("Verdict is untruthful")
        if verdict == "truthful": 
            self.overlay.evidenceText.fg = (0, 1, 0, 1)
            print("verdict is truthful")
        if verdict == "inconclusive":
            self.overlay.evidenceText.fg = (1, 1, 0, 1)
            print("verdict is inconclusive")

    def getEvidenceVerdicts(self):
        self.setEvidenceVerdict(self.game._aiController._verdictController.currentV)
        return True

    def passToVerdict(self):
        self.game._aiController._verdictController.verdictCallback(self.getEvidenceVerdicts)

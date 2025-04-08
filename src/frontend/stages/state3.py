from backend.BackendInterface.GameManager import GameManager

import os
from panda3d.core import Filename
current_dir = os.path.dirname(os.path.abspath(__file__))
prompt = os.path.join(current_dir, "..", "..", "..", "Assets", "Images", "state2contexttest.png")
prompt = os.path.normpath(prompt)
prompt = Filename.fromOsSpecific(prompt).getFullpath()

#Feel free to change this class as needed. 
class State3:
    def __init__(self):
        self.game = None
        self.state = None
        self.response = None
        self.endPhase = False
        self.overlay = None
        self.image = prompt
        self.useEmotibit = False
    
    def setGame(self, game):
        self.game = game

    def setUseEmotibit(self, useEmotibit):
        self.useEmotibit = useEmotibit

    def setOverlay(self, overlay):
        self.overlay = overlay

    def begin(self):
        self.game._gameState.updateState(3)

        self.overlay.flashback.setImage(self.image)
        self.overlay.flashback.show()
        self.overlay.hideBioData()

        flashback = self.overlay.flashback.getActive()
        while flashback == True:
            flashback = self.overlay.flashback.getActive()

        if self.useEmotibit:
            self.overlay.showBioData()
            
        self.response = self.game.generateAIResponse()
        return self.response
        
    def convert(self):
        self.game.convertTTS(self.response)
    
    def generateResponse(self):
        print("Generating response")
        self.response = self.game.generateAIResponse()

        if self.response == False:
            print("Ending phase")
            self.endPhase = True

        return self.response
    
    def introduceEvidence(self):
        self.game._aiController.introduceEvidence()

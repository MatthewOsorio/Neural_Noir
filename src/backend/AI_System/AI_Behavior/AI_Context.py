from __future__ import annotations
from .AI import AI

class AIContext():

    _state = None
    
    def __init__(self, state: AI) -> None:
        self.setAIBehavior(state)
        
    def setAIBehavior(self, state: AI):
        self._state = state
        self._state.behavior = self

    def processUserResponse(self, userResponse: str):
        self._state.processResponse(userResponse)
         
    def generateResponse(self):
        return self._state.generateResponse()
    
    def updateNervous(self, isNervous):
        self._state.updateNervous(isNervous)

    def getCurrentEvidence(self):
        print("Getting Evidence")
        if self._state._currentEvidence is not None:
            print("Evidence exists")
            return self._state._currentEvidence
        else:
            return None
from __future__ import annotations
from .AI import AI

class AIContext():

    _state = None
    
    def __init__(self, state: AI) -> None:
        self.setAIBehavior(state)
        
    def setAIBehavior(self, state: AI):
        self.state = state
        self.state.behavior = self
         
    def generateResponse(self):
        return self.state.generateResponse()
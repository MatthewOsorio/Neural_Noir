from __future__ import annotations
from . AIStateInterface import AIStateInterface

class AIBehavior():

    _state = None
    
    def __init__(self, state: AIStateInterface) -> None:
        self.setAIBehavior(state)
        
    def setAIBehavior(self, state: AIStateInterface):
        self._state = state
        self._state.behavior = self
        
    def generateResponse(self):
        self._state.generateResponse()
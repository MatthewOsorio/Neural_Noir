from .GameState import GameState

class GameStateManager:
    def __init__(self):
        self._currentState= None
        self._emotibitUsed= None
        self._stateHistory = []
        self._aiReference= None

    def setAIReference(self, ai_reference):
        self._aiReference = ai_reference

    def notifyAIReference(self):
        if self._aiReference == None:
            raise ValueError("AI reference has not been set in game state mangaer")
        else:
            self._aiReference.update(self)

    def updateState(self, state):
        try:
            newState = GameState(state)
        except ValueError:
            raise ValueError("Invalid game state ... must be within 1 - 4")
        
        if not self._currentState:
            self._currentState = newState
        else:        
            if newState == self._currentState:
                raise ValueError(f"We are currently at state ({newState.value})")
            elif newState.value in self._stateHistory:
                raise ValueError(f"We've already have been at state ({newState.value})")
            else:
                self._stateHistory.append(self._currentState.value)
                self._currentState = newState

        self.notifyAIReference()
        
    def getCurrentState(self):
        return self._currentState
    
    def getEmotibitUsed(self):
        return self._emotibitUsed
    
    def setEmotibitUsed(self, is_used):
        if isinstance(is_used, bool):
            self._emotibitUsed = is_used
        else:
            raise TypeError("Invalid Type... emotibitUsed needs True or False")
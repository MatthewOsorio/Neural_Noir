from enum import Enum

class GameState(Enum):
    initialPhase = 1       # Ask basic questions, in order to collect baseline
    earlyInterrogation = 2     # Begin real interrogation, bad cops dominates conversation and good cop plays passive role
    midInterrogation = 3    # Second part of interroation, bad cop leaves room out of frustation and good cops talks alone with suscpect
    finalInterrogation = 4 # Bad cop comes back and continues the interrogation

    def __init__(self, hasEmotibit) -> None:
        self.currentState= 1
        self.hasEmotibit= hasEmotibit

    def updateState(self, newState) -> None:
        if newState >= GameState.earlyInterrogation.value and newState <= GameState.finalInterrogation.value:
            self.currentState = newState
        else:
            raise ValueError("Invalid game state")
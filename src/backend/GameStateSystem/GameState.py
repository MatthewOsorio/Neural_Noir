from enum import Enum

class GameState(Enum):
    initialPhase = 1           # Ask basic questions, in order to collect baseline
    earlyInterrogation = 2     # Begin real interrogation, bad cops dominates conversation and good cop plays passive role
    midInterrogation = 3       # Second part of interrogation, bad cop leaves room out of frustation and good cop talks alone with suspect
    finalInterrogation = 4     # Bad cop comes back and continues the interrogation
    endGame = 5                # Verdict dictionary is passed into StoryGraph logic and end game is evaluated


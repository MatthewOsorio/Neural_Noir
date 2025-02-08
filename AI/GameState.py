from enum import Enum

class GameState(Enum):
    basic_questioning = 1       # Ask basic questions, in order to collect baseline
    first_interrogation = 2     # Begin real interrogation, bad cops dominates conversation and good cop plays passive role
    second_interrogation = 3    # Second part of interroation, bad cop leaves room out of frustation and good cops talks alone with suscpect
    finishing_interrogation = 4 # Bad cop comes back and 
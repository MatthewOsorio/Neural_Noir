from backend.BackendInterface.GameManager import GameManager
from backend.StoryGraph.EndGame import EndGame

class State5:
    def __init__(self):
        self.game = None
        self.state = None
        self.endPhase = False
        self.verdict = None

    def setGame(self, game):
        self.game = game

    def begin(self):
        self.game._gameState.updateState(5)

        endgame = EndGame(self.game._aiController._storyGraph)

        self.verdict = endgame.determineEnding()
        self.endPhase = True

        self.displayEndingScreen()

        return self.verdict
    
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


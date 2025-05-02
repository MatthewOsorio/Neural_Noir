class EndGame:
    def __init__(self, storyGraph, difficulty):
        self._storyGraph = storyGraph
        self._difficulty = difficulty

    def determineEnding(self):
        if self._difficulty == 'easy':
             finalVerdict = self._storyGraph.determineFinalVerdict()
        elif self._difficulty == 'hard':
             finalVerdict = self._storyGraph.determineFinalVerdictHardMode()
        finalVerdict = self._storyGraph.determineFinalVerdict()
        return finalVerdict
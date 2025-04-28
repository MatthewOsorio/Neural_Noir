class EndGame:
    def __init__(self, storyGraph, settings):
        self._storyGraph = storyGraph
        self._settings = settings

    def determineEnding(self):
        difficulty = self._settings.get("difficulty", "easy")

        if difficulty.lower() == 'easy':
            finalVerdict = self._storyGraph.determineFinalVerdict()
        elif difficulty.lower() == 'hard':
            finalVerdict = self._storyGraph.determineFinalVerdictHardMode()
        
        return finalVerdict
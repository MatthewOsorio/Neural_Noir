class EndGame:
    def __init__(self, storyGraph):
        self._storyGraph = storyGraph

    def determineEnding(self):
        finalVerdict = self._storyGraph.determineFinalVerdict()
        return finalVerdict
# Good-cop scenario
from .AI import AI

class AIMidInterrogation(AI):
    def __init__(self, conversation):
        super().__init__(conversation)
        self._evidence = None
        self._storyGraph = None

    def receiveEvidence(self, evidence, story_graph):
        self._evidence = evidence
        self._storyGraph = story_graph

    def returnResultToStoryGraph(self):
        pass

    # def generateResponse(self) -> str:
    #     if self._evidence == None:
            
    def setInstructions(self):
        print("mid")

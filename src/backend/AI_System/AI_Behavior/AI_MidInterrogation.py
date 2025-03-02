from .AI import AI

class AIMidInterrogation(AI):
    def __init__(self, conversation):
        super().__init__(conversation)
        self._evidence = None
        self._storyTree = None

    def recieveEvidence(self, evidence, story_tree):
        self._evidence = evidence
        self._storyTree = story_tree

    def returnResultToStoryTree(self):
        pass

    # def generateResponse(self) -> str:
    #     if self._evidence == None:
            
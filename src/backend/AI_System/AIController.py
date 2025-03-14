from .AI_Behavior import AIInitialPhase, AIEarlyInterrogation, AIMidInterrogation, AIFinalInterrogation, AIContext
from ..StoryTree.StoryTree import StoryTree

class AIController:
    def __init__(self, conversation):
        self._ai = None     
        self._conversation = conversation
        self._userNervous = None
        self._storyTree = StoryTree()

    def setAIBehavior(self, state):
        match state.value:
            case 1:
                self._ai = AIContext(AIInitialPhase(self._conversation))
            case 2:
                self._ai = AIContext(AIEarlyInterrogation(self._conversation, self._storyTree))
            case 3:
                self._ai = AIContext(AIMidInterrogation(self._conversation))
            case 4:
                self._ai = AIContext(AIFinalInterrogation(self._conversation))

    def update(self, state):
        self.setAIBehavior(state)

    def generateResponse(self):
        return self._ai.generateResponse()
    
    def processUserResponse(self, userResponse):
        self._ai.processUserResponse(userResponse)

    def updateNervous(self, isNervous):
        self._userState = isNervous
        self._ai.updateNervous(isNervous)
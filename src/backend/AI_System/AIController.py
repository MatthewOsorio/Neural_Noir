from .AI_Behavior import AIInterrogation, AIContext, AIInitialPhase
from StoryGraph.StoryGraph import StoryGraph
from .AI_History import AIHistory

class AIController:
    def __init__(self, conversation):
        self._ai = None    
        self._conversation = None 
        self._conversation = conversation
        self._aiHistory = AIHistory() 
        self._userNervous = None
        self._storyGraph = StoryGraph()

    def setAIBehavior(self, state):
        match state.value:
            case 1:
                self._ai = AIContext(AIInitialPhase(self._aiHistory))
            case 2:
                self._ai = AIContext(AIInterrogation(storyGraph= self._storyGraph, history= self._aiHistory, phase="EARLY"))
            case 3:
                self._ai = AIContext(AIInterrogation(storyGraph= self._storyGraph, history= self._aiHistory, phase="MID"))
            case 4:
                self._ai = AIContext(AIInterrogation(storyGraph= self._storyGraph, history= self._aiHistory, phase="FINAL"))

    def update(self, state):
        self.setAIBehavior(state)

    def generateResponse(self):
        return self._ai.generateResponse()
    
    def processUserResponse(self, userResponse):
        self._ai.processUserResponse(userResponse)

    def updateNervous(self, isNervous):
        self._userState = isNervous
        self._ai.updateNervous(isNervous)
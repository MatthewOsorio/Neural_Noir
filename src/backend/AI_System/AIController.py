from .AI_Behavior import AIInterrogation, AIContext, AIInitialPhase
from backend.StoryGraph.StoryGraph import StoryGraph
from .AI_History import AIHistory
from .VerdictController import VerdictController
from .SentimentAnalysis import SentimentAnalysis

class AIController:
    def __init__(self, sessionController):
        self._ai = None     
        self._userNervous = None
        self._aiHistory = AIHistory() 
        self._storyGraph = StoryGraph()
        self._verdictController = VerdictController(sessionController)
        self._sentimentAnalyzer = SentimentAnalysis()

    def setAIBehavior(self, state):
        match state.value:
            case 1:
                self._ai = AIContext(AIInitialPhase(self._aiHistory, sentimentAnalyzer=self._sentimentAnalyzer))
            case 2:
                self._ai = AIContext(AIInterrogation(storyGraph= self._storyGraph, history= self._aiHistory, phase="EARLY", verdictController=self._verdictController, sentimentAnalyzer=self._sentimentAnalyzer))
            case 3:
                self._ai = AIContext(AIInterrogation(storyGraph= self._storyGraph, history= self._aiHistory, phase="MID", verdictController=self._verdictController, sentimentAnalyzer=self._sentimentAnalyzer))
            case 4:
                self._ai = AIContext(AIInterrogation(storyGraph= self._storyGraph, history= self._aiHistory, phase="FINAL", verdictController= self._verdictController, sentimentAnalyzer=self._sentimentAnalyzer))
            case 5:
                self._ai = None

    def update(self, state):
        self.setAIBehavior(state)

    def generateResponse(self):
        return self._ai.generateResponse()
    
    def processUserResponse(self, userResponse):
        self._ai.processUserResponse(userResponse)

    def updateNervous(self, isNervous):
        self._userState = isNervous
        self._ai.updateNervous(isNervous)

    def getCurrentEvidence(self):
        return self._ai.getCurrentEvidence()
    
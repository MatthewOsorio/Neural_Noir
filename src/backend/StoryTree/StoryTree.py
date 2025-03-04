class StoryTree:
    def __init__(self):
        self._evidenceList = ['The suspect has a black eye', "Neighbor's statement that a man fitting the suspects description was at the crime scene", 'Gun with blood on it at the crime scene']
        self._currentEvidence = 0
        self._convoAboutEvidence= []
        self._aiReference = None

    def setAIReference(self, ai):
        self._aiReference = ai

    def sendEvidenceToAI(self, ai):
        if self._aiReference == None:
            self.setAIReference(ai)

        if self._aiReference == None:
            raise Exception("The AI reference has not been set yet in the Story Tree")
        
        if self._currentEvidence < len(self._evidenceList):
            evidence = self._evidenceList[self._currentEvidence]
            self._currentEvidence += 1
            return evidence
        else:
            return False

    def recieveConversation(self, convo):
        self._convoAboutEvidence.append(convo)
        
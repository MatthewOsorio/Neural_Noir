import random

class StoryGraph:
    def __init__(self):
        self._evidenceList = [
            "Crime Scene Photo of Vinh Davis – A police photograph of Vin Davis’ body with a gunshot wound.",
            "Witness Testimonies – Several written statements from bar patrons who saw MC and the CEO drinking together, with some recalling an argument.",
            "Bar Receipt – A receipt from the bar, proving that MC and the CEO were drinking heavily on the night of the murder.",
            "Blood-Stained Clothing – The police found MC’s shirt and jacket with blood stains. They ask if he remembers how it got there.",
            "Gun Matching the Bullet Wound – The murder weapon is found near the crime scene, and detectives claim it matches MC’s fingerprints.",
            "Photo of the Alleyway – A police photograph of the alleyway where MC was seen walking home, looking disoriented and covered in blood.",
            "Neighbors’ Statements – People living near MC’s apartment reported seeing him return home in a confused and unstable state.",
            "Johnny’s Last Notes – A notebook belonging to Johnny, containing scribbled messages about Vin Davis’s crimes, mentioning MC’s name.",
            "MC’s Own Camera Film – The detectives show a developed film roll from MC’s camera found at the crime scene.",
            "Police Ballistics Report – The gunshot report confirms that the weapon was fired at close range, suggesting a struggle before the CEO was shot."
        ]
        self._criticalEvidenceSet = {1, 4, 5, 9, 10}
        random.shuffle(self._evidenceList)

        self._currentEvidence = 0
        self._convoAboutEvidence = []
        self._verdictsByEvidence = {}
        self._finalVerdict = None

        # Timer, future implementation
        #self._timeElapsed = 0

        self._aiReference = None

    def setAIReference(self, ai):
        self._aiReference = ai

    def sendEvidenceToAI(self, ai):
        if self._aiReference == None:
            self.setAIReference(ai)

        if self._aiReference == None:
            raise Exception("The AI reference has not been set yet in the Story Graph")
        
        if self._currentEvidence < len(self._evidenceList):
            evidence = self._evidenceList[self._currentEvidence]
            self._currentEvidence += 1
            return evidence
        else:
            return False

    def receiveConversation(self, convo):
        self._convoAboutEvidence.append(convo)

    def receiveVerdict(self, evidenceIndex, verdict):
        verdict = verdict.upper()
        self._verdictsByEvidence[evidenceIndex] = verdict

    def determineFinalVerdict(self):
        guilty = 0
        notGuilty = 0

        # Count for each verdict type
        for verdict in self._verdictsByEvidence.values():
            if verdict == "GUILTY":
                guilty += 1
            elif verdict == "NOT GUILTY":
                notGuilty += 1

        # Defines the automatic loss ending for failing all critical evidence
        failedCriticalEvidence = 0 
        for index in self._criticalEvidenceSet:
            if self._verdictPerEvidence.get(index) == "GUILTY":
                failedCriticalEvidence += 1

        if failedCriticalEvidence == len(self._criticalEvidenceSet):
            self._finalVerdict = "GUILTY"
            return self._finalVerdict
        
        # Loss by failing 6+ pieces of evidence
        if guilty >= 6:
            self._finalVerdict = "GUILTY"
            return self._finalVerdict
        
        # Defines the the automatic win ending for sucessfully denying all critical
        # evidence and an additional evidence from the set
        deniedCritical = 0
        for index in self._criticalEvidenceSet:
            if self._verdictsByEvidence.get(index) == "NOT GUILTY":
                deniedCritical += 1

        if deniedCritical == len(self._criticalEvidenceSet) and guilty >= (len(self._criticalEvidenceSet) + 1):
            self._finalVerdict = "NOT GUILTY"
            return self._finalVerdict

        # Not guilty win condition for denying 7+ pieces of evidence
        if guilty >= 7:
            self._finalVerdict = "NOT GUILTY"
            return self._finalVerdict

        # If 30 minutes elapse without reaching a conclusion
        # if self._timeElapsed >= 30:
        #     self._finalVerdict = "INCONCLUSIVE"
        #     return "INCONCLUSIVE"

        return None 
        
    def reset(self):
        random.shuffle(self._evidenceList)
        self._currentEvidenceIndex = 0
        self._verdictPerEvidence = {}
        self._finalVerdict = None
        #self._timeElapsed = 0
        

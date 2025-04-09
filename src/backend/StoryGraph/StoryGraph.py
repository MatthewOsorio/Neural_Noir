class StoryGraph:
    def __init__(self):
        self._earlyEvidence = [
            "Crime Scene Photo of Vinh Davis – A police photograph of Vinh Davis’ body with a gunshot wound.",
            "Witness Testimonies – Several written statements from bar patrons who saw the employee and the CEO drinking together, with some recalling an argument.",
            "Bar Receipt – A receipt from the bar, proving that the employee and the CEO were drinking heavily on the night of the murder."
        ]
        self._midEvidence = [
            "Blood-Stained Clothing – The police found the employee’s shirt and jacket with blood stains. They ask if he remembers how it got there.",
            "Photo of the Alleyway – A police photograph of the alleyway where the employee was seen walking home, looking disoriented and covered in blood.",
            "Neighbors’ Statements – People living near the employee’s apartment reported seeing them return home in a confused and unstable state."
        ]
        self._finalEvidence = [
            "Gun Matching the Bullet Wound – The murder weapon is found near the crime scene, and detectives claim it matches employee’s fingerprints.",
            "Johnny’s Last Notes – A notebook belonging to Johnny, containing scribbled messages about Vinh Davis’s crimes. It also mentions the employee’s name, suggesting Johnny trusted the employee to help him.",
            "The employee’s Own Camera Film – The detectives show a developed film roll from the employee’s camera found at the crime scene, possibly containing a blurred or distorted photo from the altercation.",
            "Police Ballistics Report – The gunshot report confirms that the weapon was fired at close range, suggesting a struggle before the CEO was shot."
        ]

        self._evidencePhase = {
            "EARLY": 0,
            "MID": 0,
            "FINAL": 0
        }

        self._criticalEvidenceSet = {1, 4, 5, 9, 10}

        self._convoAboutEvidence = []
        self._verdictsByEvidence = {}
        self._finalVerdict = None

        # Timer, future implementation
        #self._timeElapsed = 0

        self._aiReference = None

    def setAIReference(self, ai):
        self._aiReference = ai

    def sendEvidenceToAI(self, ai, phase):
        if self._aiReference == None:
            self.setAIReference(ai)
        
        evidenceList = self.getEvidenceListByPhase(phase)
        index = self._evidencePhase[phase]
        
        if index < len(evidenceList):
            evidence = evidenceList[index]
            self._evidencePhase[phase] += 1
            return evidence
        else:
            return False
        
    def getEvidenceListByPhase(self, phase):
        if phase == "EARLY":
            return self._earlyEvidence
        elif phase == "MID":
            return self._midEvidence
        elif phase == "FINAL":
            return self._finalEvidence

    def receiveConversation(self, convo):
        self._convoAboutEvidence.append(convo)

    def receiveVerdict(self, evidenceKey, verdict):
        verdict = verdict.upper()
        self._verdictsByEvidence[evidenceKey] = verdict

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
        

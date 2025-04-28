class StoryGraph:
    def __init__(self):
        self._earlyEvidence = [
            ("Crime Scene Photo of Vinh Davis – A police photograph of Vinh Davis’ body with a gunshot wound.", "early1.png"),
            #("Witness Testimonies – Several written statements from bar patrons who saw the employee and the CEO drinking together, with some recalling an argument.", "early2.png"),
            #("Bar Receipt – A receipt from the bar, proving that the employee and the CEO were drinking heavily on the night of the murder.", "early3.png")
        ]
        self._midEvidence = [
            ("Blood-Stained Clothing – The police found the employee’s shirt and jacket with blood stains. They ask if he remembers how it got there.", "mid1.png"),
            #("Photo of the Alleyway – A police photograph of the alleyway where the employee was seen walking home, looking disoriented and covered in blood.", "mid2.png"),
            #("Neighbors’ Statements – People living near the employee’s apartment reported seeing them return home in a confused and unstable state.", "mid3.png")
        ]
        self._finalEvidence = [
            ("Gun Matching the Bullet Wound – The murder weapon is found near the crime scene, and detectives claim it matches employee’s fingerprints.", "final1.png"),
            #("Johnny’s Last Notes – A notebook belonging to Johnny, containing scribbled messages about Vinh Davis’s crimes. It also mentions the employee’s name, suggesting Johnny trusted the employee to help him.", "final2.png"),
            #("The employee’s Own Camera Film – The detectives show a developed film roll from the employee’s camera found at the crime scene, possibly containing a blurred or distorted photo from the altercation.", "final3.png"),
            #("Police Ballistics Report – The gunshot report confirms that the weapon was fired at close range, suggesting a struggle before the CEO was shot.", "final4.png")
        ]

        self._evidencePhase = {
            "EARLY": 0,
            "MID": 0,
            "FINAL": 0
        }

        self._criticalEvidenceSet = {1, 4, 5, 9, 10}

        self._verdictsByEvidence = {}
        self._finalVerdict = None

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

    '''
    Notes from Matt:
        I changed the recieve verdict a bit. Here we find the index of the current evidence and save it into the self._verdictsByEvidence dict.
        This is exaclty what is being stored in there:
            {EARLY-1': 'INCONCLUSIVE', 'EARLY-2': 'UNTRUTHFUL', 'EARLY-3': 'UNTRUTHFUL', ....}
    '''
    def receiveVerdict(self, currentEvidence, verdict, phase):
        verdict = verdict.upper()
        currentEvidenceList = self.getEvidenceListByPhase(phase)
        currentEvidenceIndex = currentEvidenceList.index(currentEvidence) + 1
        self._verdictsByEvidence[f"{phase}-{currentEvidenceIndex}"] = verdict

    def determineFinalVerdict(self):
        guilty = 0
        notGuilty = 0
        inconclusive = 0

        # Count for each verdict type
        for verdict in self._verdictsByEvidence.values():
            if verdict == "UNTRUTHFUL":
                guilty += 1
            elif verdict == "TRUTHFUL":
                notGuilty += 1
            elif verdict == "INCONCLUSIVE":
                inconclusive += 1

        criticalFailure = 0
        criticalSuccess = 0

        for phase in ["EARLY", "MID", "FINAL"]:
            for id in self._criticalEvidenceSet:
                key = f"{phase}-{id}"
                if key in self._verdictsByEvidence:
                    verdict = self._verdictsByEvidence[key]
                    if verdict == "UNTRUTHFUL":
                        criticalFailure += 1
                    elif verdict == "TRUTHFUL":
                        criticalSuccess += 1

        # Defines the automatic loss ending for failing all critical evidence
        if criticalFailure == len(self._criticalEvidenceSet):
            self._finalVerdict = "GUILTY"
            return "GUILTY"
        
        # Loss by failing 6+ pieces of evidence
        if guilty >= 6:
            self._finalVerdict = "GUILTY"
            return "GUILTY"
        
        # Defines the the automatic win ending for successfully denying all critical
        # evidence and an additional evidence from the set
        if criticalSuccess == len(self._criticalEvidenceSet) and notGuilty>= 6:
            self._finalVerdict = "NOT GUILTY"
            return "NOT GUILTY"
        
        # Not guilty win condition for denying 7+ pieces of evidence
        if notGuilty >= 7:
            self._finalVerdict = "NOT GUILTY"
            return "NOT GUILTY"

        # No conditions met results in inconclusive
        self._finalVerdict = "INCONCLUSIVE"
        return "INCONCLUSIVE"
    
    def determineFinalVerdictHardMode(self):
        guilty = 0
        notGuilty = 0
        inconclusive = 0

        # Count for each verdict type
        for verdict in self._verdictsByEvidence.values():
            if verdict == "UNTRUTHFUL":
                guilty += 1
            elif verdict == "TRUTHFUL":
                notGuilty += 1
            elif verdict == "INCONCLUSIVE":
                inconclusive += 1

        criticalFailure = 0
        criticalSuccess = 0

        for phase in ["EARLY", "MID", "FINAL"]:
            for id in self._criticalEvidenceSet:
                key = f"{phase}-{id}"
                if key in self._verdictsByEvidence:
                    verdict = self._verdictsByEvidence[key]
                    if verdict == "UNTRUTHFUL":
                        criticalFailure += 1
                    elif verdict == "TRUTHFUL":
                        criticalSuccess += 1

        # Defines the automatic loss ending for failing all critical evidence
        if criticalFailure == len(self._criticalEvidenceSet):
            self._finalVerdict = "GUILTY"
            return "GUILTY"
        
        # Loss by failing 4+ pieces of evidence
        if guilty >= 4:
            self._finalVerdict = "GUILTY"
            return "GUILTY"
        
        # Defines the the automatic win ending for successfully denying all critical
        # evidence and an additional evidence from the set
        if criticalSuccess == len(self._criticalEvidenceSet) and notGuilty>= 4:
            self._finalVerdict = "NOT GUILTY"
            return "NOT GUILTY"
        
        # Not guilty win condition for denying 8+ pieces of evidence
        if notGuilty >= 8:
            self._finalVerdict = "NOT GUILTY"
            return "NOT GUILTY"

        # No conditions met results in inconclusive
        self._finalVerdict = "INCONCLUSIVE"
        return "INCONCLUSIVE"
        

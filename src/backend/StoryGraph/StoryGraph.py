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
        random.shuffle(self._evidenceList)
        
        self._currentEvidence = 0
        self._convoAboutEvidence = []
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

    def receiveConversation(self, convo):
        self._convoAboutEvidence.append(convo)
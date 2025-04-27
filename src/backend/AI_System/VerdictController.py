from openai import OpenAI
from textwrap import dedent
from threading import Thread
import json
import re

class VerdictController:
    def __init__(self, sessionController):
        self._gpt = OpenAI()
        self.callbackF = None
        self._sessionController = sessionController
        self.currentV = None

    # Purpose: requesting GPT to dervice a verdict from the conversation
    def deriveVerdict(self, interrogation, evidenceConvo, evidence):
        cleanEvidenceConvo = '\n'.join(line.strip() for line in evidenceConvo)

        gptInput = dedent(f"""[INSTRUCTION] You are evaluating whether the suspect, Mark Coleman, was honest about the following piece of evidence:

        [EVIDENCE] {evidence}

        You may use the full conversation history to spot contradictions or inconsistencies.

        Below is the portion of the conversation directly related to this evidence:

        {cleanEvidenceConvo}

        Return a JSON object with two fields:
        - "verdict": Must be one of the following strings: "truthful", "untruthful", or "inconclusive"
        - "reasoning": A concise explanation (1-3 sentences) justifying the verdict

        **RULES**
        - Please explain your reasoning.
        - DO NOT roleplay or speak as a character.
        - DO NOT include anything except the verdict tag.
        - Only judge the suspect's honesty about the listed evidence.
        """)

        interrogation.append({'role': 'user', 'content': gptInput})
        gptResponse = self._gpt.chat.completions.create(
            model='gpt-4o-mini',
            messages=interrogation
        )

        rawResponse = gptResponse.choices[0].message.content
        cleanedResponse = re.sub(r"^```(?:json)?\s*|\s*```$", "", rawResponse.strip(), flags=re.IGNORECASE | re.MULTILINE)

        responseDict = json.loads(cleanedResponse)
        currentVerdict = responseDict.get("verdict", "inconclusive").lower()

        self.sendVerdictToDB(evidence, currentVerdict)
        print(f"Verdict control verdict for {evidence} = {currentVerdict}")
        self.currentV = currentVerdict
        self.callbackF()
        return currentVerdict

    
    #For the evidence text color change
    def verdictCallback(self, callback):
        self.callbackF = None
        self.callbackF = callback

    # Purpose: Sending verdict to database on a separate thread
    def sendVerdictToDB(self, evidence, verdict):
        databaseThread = Threakd(target=self._sessionController.databaseAPI.insertVerdict, args=(self._sessionController.getSessionID(), evidence, verdict), daemon=True)
        databaseThread.start()
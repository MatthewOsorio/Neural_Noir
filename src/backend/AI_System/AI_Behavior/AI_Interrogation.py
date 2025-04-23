from textwrap import dedent
from .AI import AI

class AIInterrogation(AI):
    def __init__(self, storyGraph, history, phase, verdictController, sentimentAnalyzer):
        super().__init__(history)
        self._storyGraph = storyGraph
        self._phase = phase
        self._verdictController = verdictController
        self._sentimentAnalyzer = sentimentAnalyzer

        self._currentEvidence = None
        self._introducedEvidence = False
        self._doneWithCurrentEvidence = False

        self._aiResponse = None
        self._evidenceConversation = []
        self._counter = 0
        self._finish = False

    # Purpose: Requesting evidence from story graph based on the current phase of the AI
    def receiveEvidence(self):
        if self._storyGraph == None:
            raise Exception("Story Graph reference has not been set")

        self._currentEvidence = self._storyGraph.sendEvidenceToAI(self, self._phase)
        
        if self._currentEvidence == False:
            self._finish = True

    # Purpose: Sending a prompt to GPT to smoothly introduce a peiece of evidence and returning that response
    def introduceEvidence(self):
        if self._currentEvidence is None:
            self.receiveEvidence()
            print("Reset")
            self._verdictController.currentVerdict = None

            if self._finish:
                return False
        
        gptInput= self._aiHistory.getHistory()[:]
        
        prompt= dedent(f'''[INSTRUCTION] Introduce this piece of evidence: {self._currentEvidence}. Follow the rules below:

                **RULES**
                    - If this is the first piece of evidence in the interrogation, begin questioning the suspect about it directly.
                    - If this is not the first piece of evidence, begin by smoothly transitioning from the previous topic — make the shift feel like a natural continuation of the interrogation.
                    - Then, ask the suspect what they know about this specific piece of evidence.
                    - If the evidence was found at the crime scene, briefly mention that.
                    - Respond as either or both detectives, staying fully in character.
                    - Both detectives may speak, but they must stay focused on this specific item.
                    - Do NOT discuss any other evidence or unrelated topics.
                    - Be concise.
                    - Only ask UP TO three follow up questions per piece of evidence. There can be less if a verdict is possible before hitting three, but DO NOT go over three''')
        
        instruction = {'role': 'user', 'content': prompt}
        gptInput.append(instruction)
        gptResponse = self.sendToGPT(gptInput)
        self.addAIResponsesToEvidenceCono(gptResponse)
        self._introducedEvidence = True
        self.classifyDetectivesSentiment()

        return gptResponse
            
    # Purpose: Store the AI responses in the evidence conversation list in a transcript format
    def addAIResponsesToEvidenceCono(self, response):
        for response in response:
            self._evidenceConversation.append("Detective " + response["Speaker"] + ": " + response["Text"])

    # Purpose: Managing what kind of response will be returned from the AI
    #   If we have not introduced evidence, then the AI will introduce it.
    #   If we are not introducing evidence, then the AI will return whatever is stored in aiResponses which is GPTs response to the user from the processResponse method 
    #   After three turns the AI will generate a verdict from the evidence conversation and then move on to the next piece of evidence
    #   When we have exhuasted all the evidence in the current phase we will return false
    def generateResponse(self): 
        if self._finish: 
            self.generateVerdict()
            self._verdictController.callbackF()
            return False

        if not self._introducedEvidence:
            return self.introduceEvidence()
        
        if self._counter == 3:
            self.generateVerdict()
            self._verdictController.callbackF()
            self.moveOnToNextTopic()
            
            return self.introduceEvidence()
        
        return self._aiResponse

    # Purpose: Receive the users input and format it in the desired format. Create the prompt for GPT and send it to GPT.
    #   If we have processed the users response three times it will not generate another response because we will begin the process of moving on to the next piece of evidence and verdict generation
    def processResponse(self, userResponse):
        gptInput = self._aiHistory.getHistory()[:]
        preppedResponse = "[MARK]: " + userResponse
        self._aiHistory.addUserInput(preppedResponse)
        self._evidenceConversation.append(preppedResponse)

        if self._counter == 2:
            self._counter += 1
            print("Halting further GPT responses.")
            return

        instruction = dedent(f"""[INSTRUCTION] The suspect gave the following response: "{preppedResponse}"
                    The suspect appeared {'nervous' if self.userNervous else 'not nervous'} while responding.

                    [EVIDENCE] {self._currentEvidence}

                    **RULES**
                    - Respond as Detective Harris and/or Detective Miller.
                    - First, react to the suspect's explanation (skepticism, encouragement, or confrontation based on character).
                    - Then, ask exactly ONE follow-up question about this piece of evidence.
                    - Both detectives may speak — either together or back-to-back — but they must stay on the same topic.
                    - Do NOT ask two separate questions.
                    - If the suspect seemed nervous, acknowledge it in your tone or commentary.
                    - If the suspect's response is dishonest, evasive, or contradictory, point it out.
                    - DO NOT reference other evidence, the suspect's injuries, or the night of the murder.
                    - Stay fully in character: Harris is aggressive and skeptical; Miller is empathetic and calm.
                    - Be concise.
                    - End your turn after the question. Wait for the suspect's next reply before continuing.
                    """)
        
        gptInput.append({"role": 'user', 'content': instruction})

        gptResponse = self.sendToGPT(gptInput)
        
        self.addAIResponsesToEvidenceCono(gptResponse)
        self._aiResponse = gptResponse
        self._counter += 1

        self.classifyDetectivesSentiment()

    
    # Purpose: Calling the deriveVerdict method in the verdictController to send to GPT to get a verdict on current evidence conversation
    #   Then we send the verdict and the necessary information to store it in the story graph
    def generateVerdict(self):
        verdict = self._verdictController.deriveVerdict(self._aiHistory.getHistory()[:], self._evidenceConversation, self._currentEvidence)
        self._storyGraph.receiveVerdict(self._currentEvidence, verdict, self._phase)

    # Purpose: Classifies sentiment of the detective response to the player's response to the evidence
    def classifyDetectivesSentiment (self):
        lastTwoResponses = self._aiResponse[-2:]
        self.sentiment = self._sentimentAnalyzer.classifyEachDetective(lastTwoResponses)

    # Purpose: Once we have finsihed talking about our current evidence we will begin the process of talking about another piece of evidence by reseting the counter and states thats responsible for evidence mangagement
    def moveOnToNextTopic(self):
        self._currentEvidence = None
        self._counter = 0
        self._introducedEvidence = False
        self._evidenceConversation.clear()

    def setCurrentVerdict(self):
        #print(f"Current verdict: {self._verdictController.currentVerdict}")
        match = re.search(r'\[\[verdict:\s*(truthful|untruthful|inconclusive)\s*\]\]', self._verdictController.currentVerdict.lower())
        if match:
            self.currentVerdict = match.group(1)
        else:
            self.currentVerdict = "inconclusive"

    def getCurrentVerdict(self):
        print(f"Getting verdict from AI interrogation - {self.currentVerdict}")
        return self.currentVerdict
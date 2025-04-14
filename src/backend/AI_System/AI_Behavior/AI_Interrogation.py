# Bad cop scenario
import re
from textwrap import dedent
from .AI import AI

class AIInterrogation(AI):
    def __init__(self, storyGraph, history, phase):
        super().__init__(history)
        self._storyGraph = storyGraph
        self._phase = phase

        self._currentEvidence = None
        self._introducedEvidence = False

        self._aiResponse = None
        self._evidenceConversation = []
        self._counter = 0
        self._finish = False

        self._verdictKeyword = None
        self._verdict = {}

    # Requesting evidence based on phase, 
    def receiveEvidence(self):
        if self._storyGraph == None:
            raise Exception("Story Graph reference has not been set")

        self._currentEvidence = self._storyGraph.sendEvidenceToAI(self, self._phase)
        if self._currentEvidence == False:
            self._finish = True

    def introduceEvidence(self):
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
                    - Be concise.''')
        
        instruction = {'role': 'user', 'content': prompt}
        gptInput.append(instruction)
        gptResponse = self.sendToGPT(gptInput)
        self._aiResponse = gptResponse

    def sendConversationToStoryGraph(self):
        if self._storyGraph == None:
            raise Exception("Story Graph reference has not been set")

        self._storyGraph.receiveConversation(self._evidenceConversation)
        self._evidenceConversation.clear()

    # This code returns a response after a verdict has been decided. That is not supposed to happen. 
    def generateResponse(self):    
        if self._currentEvidence == None:
            self.receiveEvidence()
        
        if self._finish:
            return False

        if not self._introducedEvidence:
            self._introducedEvidence = True
            self.introduceEvidence()
        
        if self._counter == 3:
            print(self._aiHistory.getHistory())
            # self.generateVerdict()
            # self.sendConversationToStoryGraph()
            self.moveOnToNextTopic()
            # print(f"\n Verdicts so far: {self._verdict}\n")
        
        return self._aiResponse
        
    def processResponse(self, userResponse):
        gptInput = self._aiHistory.getHistory()[:]
        preppedResponse = "[MARK] " + userResponse
        self._aiHistory.addUserInput(preppedResponse)
        instruction = dedent(f"""[INSTRUCTION] The suspect gave the following response: "{preppedResponse}"
                    The suspect appeared {'nervous' if self.userNervous else 'not nervous'} while responding.

                    [EVIDENCE] {self._currentEvidence}

                    **RULES**
                    - Respond as Detective Harris and/or Detective Miller.
                    - First, react to the suspect's explanation (skepticism, encouragement, or confrontation based on character).
                    - Then, ask exactly ONE follow-up question about this piece of evidence.
                    - Both detectives may speak — either together or back-to-back — but they must stay on the same topic.
                    - Do NOT ask two separate questions in the same response.
                    - If the suspect seemed nervous, acknowledge it in your tone or commentary.
                    - If the suspect’s response is dishonest, evasive, or contradictory, point it out.
                    - DO NOT reference other evidence, the suspect's injuries, or the night of the murder.
                    - Stay fully in character: Harris is aggressive and skeptical; Miller is empathetic and calm.
                    - Be concise.
                    - End your turn after the question. Wait for the suspect’s next reply before continuing.
                    """)
        
        gptInput.append({"role": 'user', 'content': instruction})

        gptResponse = self.sendToGPT(gptInput)
        self._aiResponse = gptResponse
        self._counter += 1

    def generateVerdict(self):
        verdict = self.getVerdictFromConvo()
        self._verdictKeyword = verdict

        evidenceList = self._storyGraph.getEvidenceListByPhase(self._phase)
        curEvidenceIndex = evidenceList.index(self._currentEvidence) + 1
        self.recordVerdict(curEvidenceIndex, verdict)

    def getVerdictFromConvo(self):
        convo = self._evidenceConversation[:]

        prompt = f'''You are going to analyze the conversation between the detective and the suspect.
                    At the end, return only ONE word verdict (truthful, untruthful, or inconclusive) based on the suspect's answers.

                    **Return Format (MUST be one of):**
                    [[verdict: truthful]]
                    [[verdict: untruthful]]
                    [[verdict: inconclusive]]

                    Do NOT explain. Do NOT roleplay. Just output the tag above.
                    '''
        convo.append({'role': 'assistant', 'content': prompt})
        verdictResponse = self.sendToGPT(convo)

        match = re.search(r'\[\[verdict:\s*(truthful|untruthful|inconclusive)\s*\]\]', verdictResponse.lower())
        if match:
            return match.group(1)
        else:
            return "inconclusive"

    def recordVerdict(self, index, verdict):
        self._verdict[index] = verdict

    def reset(self):
        self._currentEvidence = None
        self._introducedEvidence = False
        self._evidenceConversation.clear()

    def addUserStatementToConvo(self, statement):
        temp = {'role': 'user', 'content': statement}
        self._evidenceConversation.append(temp)

    def addAIResponseToConvo(self, statement):
        temp = {'role': 'assistant', 'content': statement}
        self._evidenceConversation.append(temp)

    # def setupConvo(self):
    #     context = self.conversation.getContext()
    #     self._evidenceConversation.append(context)

    def moveOnToNextTopic(self):
        self._currentEvidence = None
        self._counter = 0
        self._introducedEvidence = False
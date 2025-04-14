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
        # self._evidenceConversation = []
        self._counter = 0
        self._finish = False

        # self._evidenceQueue = []
        # self._playerResponses = {}

        self._verdictKeyword = None
        self._verdict = {}

        # self.setupConvo()

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
                    - Ask the suspect what they know about this specific piece of evidence.
                    - If the evidence was found at the crime scene, briefly mention that.
                    - Do NOT discuss any other evidence. Do NOT refer to anything unrelated to this item.
                    - Wait for the suspect's response before saying more.''')
        
        instruction = {'role': 'user', 'content': prompt}
        gptInput.append(instruction)
        gptResponse = self.sendToGPT(gptInput)
        return gptResponse

    def sendConversationToStoryGraph(self):
        if self._storyGraph == None:
            raise Exception("Story Graph reference has not been set")

        self._storyGraph.receiveConversation(self._evidenceConversation)
        self._evidenceConversation.clear()
        self.setupConvo()

    ## This method just returns whatever is stored in the aiResponse attribute.
    # That attribute gets set when we introduce the evidence or the ai response to the user input
    def generateResponse(self) -> str:    
        if self._currentEvidence == None:
            self.receiveEvidence()
        
        if self._finish:
            return False

        if not self._introducedEvidence:
            self._introducedEvidence = True
            self._aiResponse = self.introduceEvidence()
        
        if self._counter == 3:
            self.sendConversationToStoryGraph()
            self.moveOnToNextTopic()
            print(f"\n Verdicts so far: {self._verdict}\n")
        
        return self._aiResponse
        
    def processResponse(self, userResponse):
        gptInput = self._aiHistory.getHistory()[:]
        preppedResponse = "[MARK] " + userResponse

        instruction = dedent(f'''[INSTRUCTION] This is the suspect's explanation of the current evidence: "{preppedResponse}".
                    The suspect appeared {'nervous' if self.userNervous else 'not nervous'} when responding.

                    [EVIDENCE] {self._currentEvidence}

                    **RULES**
                    - First, comment on the suspect's explanation.
                    - Then, ask exactly ONE follow-up question to get more detail about this piece of evidence.
                    - Both detectives must remain focused on the current evidence. Do not have them both ask questions at the same time. They may reinforce each other, apply pressure, or rephrase the same question, but never change the topic.
                    - If the suspect seemed nervous, make note of it.
                    - If the suspect's response seems dishonest or inconsistent, call it out.
                    - DO NOT discuss other evidence, the suspect's physical appearance (bruises, black eye), or any unrelated topics.
                    - DO NOT reference the night of the murder or past altercations.
                    - Stay fully in character and be concise.
                    - DO NOT ask more than one question or change the topic.''')
        
        
        gptInput.append({"role": 'user', 'content': instruction})

        gpt_response = self.sendToGPT(gptInput)
        self._aiResponse = gpt_response

        if self._counter == 2:
            #Potentially utilize threading for this
            #Also potentially decouple this process and perform it in stroy graph or make it another process
            verdict = self.getVerdictFromConvo()
            self._verdictKeyword = verdict

            evidenceList = self._storyGraph.getEvidenceListByPhase(self._phase)
            curEvidenceIndex = evidenceList.index(self._currentEvidence) + 1
            self.recordVerdict(curEvidenceIndex, verdict)

        self._counter += 1

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
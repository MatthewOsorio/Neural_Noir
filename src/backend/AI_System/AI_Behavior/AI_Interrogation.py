# Bad cop scenario
import re
from .AI import AI

class AIInterrogation(AI):
    def __init__(self, conversation, storyGraph, history, phase):
        super().__init__(conversation)
        self._storyGraph = storyGraph
        self._history = history
        self._phase = phase

        self._currentEvidence = None
        self._introducedEvidence = False

        self._aiResponse = None
        self._evidenceConversation = []
        self._counter = 0
        self._finish = False

        self._evidenceQueue = []
        self._playerResponses = {}

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
        gpt_prompt= self.conversation.getConversation()[:]

        prompt= f'''[INSTRUCTION] Introduce this piece of evidence {self._currentEvidence}. Follow the rules below:
                    **RULES**
                        - Ask the suspect what they know about the piece of evidence. 
                        - If the evidence was found at the crime scene mention that. 
                        - **ONLY TALK ABOUT THE CURRENT EVIDENCE. DO NOT MENTION ANY OTHER EVIDENCE'''
        
        instruction = {'role': 'user', 'content': prompt}

        gpt_prompt.append(instruction)
        gpt_response = self.sendToGPT(gpt_prompt)
        print("THIS IS WHAT GPT SAYS: ")
        self.addAIResponseToConvo(gpt_response)
        self._aiResponse = gpt_response

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
            self.introduceEvidence()
        
        if self._counter == 3:
            self.sendConversationToStoryGraph()
            self.moveOnToNextTopic()
            print(f"\n Verdicts so far: {self._verdict}\n")
        
        return self._aiResponse
        
    def processResponse(self, userResponse):
        # self.conversation.addUserInput(userResponse)
        self.addUserStatementToConvo(userResponse)

        prompt= f'''This is the users explanation about evidence that has been presented: {userResponse}.
                    The user was {'nervous' if self.userNervous else 'not nervous'} when giving their response.
                    Respond to the users explanation according to the rules below.
                    
                    **RULES**
                        - Respond as Detective Harris.
                        - First make a comment about their response. Then ask **only one** question to get more details before moving on to the next evidence.
                        - If the user was nervous point out it out in your response.
                        - Be concise in your response
                        - If you catch the user in a lie. Point it out in your response.
                        - Respond as if are Detective Harris.
                        - **ONLY TALK ABOUT THE EVIDENCE**
                        - **DO NOT ASK QUESTIONS UNRELATED TO THE EVIDENCE**
                        - **DO NOT MENTION MARKS, BRUISES, AND BLACK EYE**
                    ''' 
        gpt_prompt= self.conversation.getConversation()[:]
        instruction = {'role':  'assistant', 'content': prompt}
        gpt_prompt.append(instruction)

        gpt_response = self.sendToGPT(gpt_prompt)
        self.addAIResponseToConvo(gpt_response)
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
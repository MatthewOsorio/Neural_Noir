# Bad cop scenario
import random
from .AI import AI

class AIMidInterrogation(AI):
    def __init__(self, conversation, storyGraph, phase="MID"):
        super().__init__(conversation)
        self._storyGraph = storyGraph
        self._phase = phase

        self._currentEvidence = None
        self._introducedEvidence = False
        self._aiResponse = None
        self._evidenceConversation = []
        self._counter = 0
        self._finish = False

        self._evidenceQueue = []
        self._playerResponses = {}

        self.setupConvo()

    def receiveEvidence(self):
        if self._storyGraph == None:
            raise Exception("Story Graph reference has not been set")

        self._currentEvidence = self._storyGraph.sendEvidenceToAI(self, self._phase)
        if self._currentEvidence == False:
            self._finish = True

    def sendConversationToStoryGraph(self):
        if self._storyGraph == None:
            raise Exception("Story Graph reference has not been set")

        self._storyGraph.receiveConversation(self._evidenceConversation)
        self._evidenceConversation.clear()
        self.setupConvo()

    ## This method just returns whatever is stored in the aiResponse attribute. That attributes gets set when we introduce the evidence or the ai response to the user input
    def generateResponse(self) -> str:    
        if self._currentEvidence == None:
            self.receiveEvidence()
        
        if self._finish:
            return False

        if not self._introducedEvidence:
            self._introducedEvidence= True
            self.introduceEvidence()
        
        if self._counter == 3:
            self.sendConversationToStoryGraph()
            self.moveOnToNextTopic()
        
        return self._aiResponse
        
    def processResponse(self, userResponse):
        self.conversation.addUserInput(userResponse)
        self.addUserStatementToConvo(userResponse)

        # Need to change prompt according to plot rules - good cop scenario
        prompt= f'''This is the users explanation about evidence that has been presented: {userResponse}.
                    The user was {'nervous' if self.userNervous else 'not nervous'} when giving their response.
                    Respond to the users explanation according to the rules below.
                    
                    **RULES**
                        - Respond as Detective Miller.
                        - First make a comment about their response. Then ask **only one** question to get more details before moving on to the next evidence.
                        - If the user was nervous point out it out in your response.
                        - Be concise in your response
                        - If you catch the user in a lie. Point it out in your response.
                        - Respond as if are Detective Miller.
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
        self._counter += 1

    def introduceEvidence(self):
        gpt_prompt= self.conversation.getConversation()[:]

        prompt= f'''You are going to introduce this piece of evidence: {self._currentEvidence}. Follow the rules below:
                    **RULES**
                        - Ask the suspect what they know about the piece of evidence. 
                        - If the evidence was found at the crime scene mention that. 
                        - **ONLY** respond as Miller.
                        - **ONLY MENTION THE CURRENT EVIDENCE. DO NOT MENTION ANY OTHER EVIDENCE'''
        instruction = {'role': 'assistant', 'content': prompt}
        gpt_prompt.append(instruction)

        gpt_response = self.sendToGPT(gpt_prompt)

        self.addAIResponseToConvo(gpt_response)
        self._aiResponse = gpt_response
    
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

    def setupConvo(self):
        context = self.conversation.getContext()
        self._evidenceConversation.append(context)

    def moveOnToNextTopic(self):
        self._currentEvidence = None
        self._counter = 0
        self._introducedEvidence = False
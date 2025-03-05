# Good cop-Bad cop scenario
from .AI import AI

class AIEarlyInterrogation(AI):
    def __init__(self, conversation, storyTree):
        super().__init__(conversation)
        self._currentEvidence = None
        self._storyTree = storyTree
        self._introducedEvidence = False
        self._aiResponse= None
        self._evidenceConversation= []
        self._counter= 0
        self._finish = False

        self.setupConvo()

    def recieveEvidence(self):
        if self._storyTree == None:
            raise Exception("Story Tree refernce has not been set")

        self._currentEvidence = self._storyTree.sendEvidenceToAI(self)
        if self._currentEvidence == False:
            self._finish = True

    def sendConversationToStoryTree(self):
        if self._storyTree == None:
            raise Exception("Story Tree refernce has not been set")

        self._storyTree.recieveConversation(self._evidenceConversation)
        self._evidenceConversation.clear()
        self.setupConvo()

    ## This method just returns whatever is stored in the aiResponse attribute. That attributes gets set when we introduce the evidence or the ai response to the user input
    def generateResponse(self) -> str:    
        if self._currentEvidence == None:
            self.recieveEvidence()
        
        if self._finish:
            return False

        if not self._introducedEvidence:
            self._introducedEvidence= True
            self.introduceEvidence()
        
        if self._counter == 3:
            self.sendConversationToStoryTree()
            self.moveOnToNextTopic()
        
        return self._aiResponse
        
    def processResponse(self, userResponse):
        self.conversation.addUserInput(userResponse)
        self.addUserStatementToConvo(userResponse)

        prompt= f'''This is the users explanation about evidence that has been presented: {userResponse}.
                    The user was {'nervous' if self.userNervous else 'not nervous'} when giving their response.
                    Respond to the users explanation according to the rules below.
                    
                    **RULES**
                        - First make a comment about their response. Then ask **only one** question to get more details. Respond as Harris.
                        - If the user was nervous point out it out in your response.
                        - Be concise in your response
                        - If you catch the user in a lie. Point it out in your response.
                        - Respond as if are Detective Harris
                        - **ONLY TALK ABOUT THE EVIDENCE**
                        - **DO NOT ASK QUESTIONS UNRELATED TO THE EVIDENCE**
                        - **DO NOT MENTIONS MARKS BRUISES AND BLACK EYE**
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

        prompt= f'''You are going to introduce this peice of evidence: {self._currentEvidence}. Follow the rules below:

                    **RULES**
                        -Then ask the suspect what they know about the piece of evidence. 
                        - If the evidence was found at the crime scence mention that. 
                        - **ONLY** respond as Harris.
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
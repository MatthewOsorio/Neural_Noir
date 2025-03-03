from .AI import AI

class AIEarlyInterrogation(AI):
    def __init__(self, conversation):
        super().__init__(conversation)
        self._currentEvidence = 'Gun with blood on it'
        self._storyTree = "temp"
        self._introducedEvidence = False
        self._aiResponse= None
        self._evidenceConversation= []

    def setStoryTreeReference(self, storyTree):
        self._storyTree = storyTree

    def recieveEvidence(self, newEvidence):
        self._currentEvidence = newEvidence

    def sendConversationToStoryTree(self):
        pass

    ## This method just returns whatever is stored in the aiResponse attribute. That attributes gets set when we introduce the evidence or the ai response to the user input
    def generateResponse(self) -> str:
        if self._currentEvidence == None:
            raise Exception("The evidence has not been set yet. Invoke receiveEvidence(evidence) method in the story tree")
        
        if self._storyTree == None:
            raise Exception("The story tree reference has not been set yet. Invoke the setStoryTreeReference(storyTree) method in AI Controller")
        
        if not self._introducedEvidence:
            self.introduceEvidence()
            self._introducedEvidence= True

        return self._aiResponse
        
    def processResponse(self, userResponse):
        clean_user_response= 'Player: ' + userResponse
        self.conversation.addUserInput(userResponse)

        self.addToConvo(clean_user_response)

        prompt= f'''This is the users explanation about evidence that has been presented: {userResponse}
                    Respond to the users explanation according to the rules below.
                    
                    **RULES**
                        - If the users explanation is vague tell them to be more specific. Respond as both Harris and Miller but make it natural.
                        - If the users explanation is reasonable ask them for details in about explanation. Respond as both Harris and Miller but make it natural.
                        - If the user is being evasive, tell them to stop evading. Respond as Harris and *do not* respond as Miller.
                        - If the user explanation is irrelevant or unrelated, tell them stop messing around. Respond as Harris and *do not* respond as Miller.
                        - If the user seems scared, reasure them. Respond as Miller and *do not* respond as Harris
                        - **ONLY TALK ABOUT THE EVIDENCE**
                        - **DO NOT ASK QUESTIONS UNRELATED TO THE EVIDENCE**
                        - **DO NOT MENTIONS MARKS BRUISES AND BLACK EYE**
                    ''' 
        
        gpt_prompt= self.conversation.getConversation()[:]
        instruction = {'role':  'assistant', 'content': prompt}
        gpt_prompt.append(instruction)

        gpt_response = self.sendToGPT(gpt_prompt)
        
        self._aiResponse = gpt_response

    def introduceEvidence(self):
        gpt_prompt= self.conversation.getConversation()[:]
        prompt= f'You are going to introduce this peice of evidence: {self._currentEvidence}, It was found at a crime scence. Then ask the suspect what they know about the piece of evidence. Respond as Harris and **do not** respond as Miller.'
        instruction = {'role': 'assistant', 'content': prompt}
        gpt_prompt.append(instruction)

        gpt_response = self.sendToGPT(gpt_prompt)

        self.addToConvo(gpt_response)
        self._aiResponse = gpt_response
    
    def reset(self):
        self._currentEvidence = None
        self._introducedEvidence = False
        self._evidenceConversation.clear()

    def addToConvo(self, statement):
        self._evidenceConversation.append(statement)

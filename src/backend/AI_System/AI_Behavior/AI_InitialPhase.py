# Initial state - detectives ask the intro questions and EmotiBit baseline is taken
from .AI import AI

class AIInitialPhase(AI):
    def __init__(self, conversation):
        super().__init__(conversation)
        self._questions= [
            'Harris: What is your name?',
            'Harris: Do you work at the Reno Times?',
            'Harris: Do you work as a journalist?',
            'Harris: Did you work for Vinh Davis?'
        ]
        self._finished = False
        self._currentQuestion = 0

    def askQuestion(self):
        if self._finished:
            return 
        
        question = self._questions[self._currentQuestion]
        self.conversation.addAIResponse(question)
        return question
    
    def processResponse(self, userResponse):
        self.conversation.addUserInput(userResponse)
        gpt_response = self.evaluateResponse(userResponse)

        if 'Correct' in gpt_response:
            self._currentQuestion += 1
            self.askedAllQuestions()
        else:
            self._questions[self._currentQuestion] = gpt_response

    def evaluateResponse(self, user_response):
        prompt= ''

        if self._currentQuestion == 0:
            prompt = f'''
                        Based on the current information you have verify the users response: {user_response}.
                        Determine if it aligns with the current information you have.
                        
                        **Rules**
                            - Only respond as Harris.
                            - If the answer is correct **respond with Correct**
                            - If the the user's response is slightly misspelled **respond with Correct**
                            - TREAT 'Mark' AND 'Marc'AS THE SAME NAME **respond with Correct**
                            - Once you respond with "Correct" **do not** ask another question 
                            - If the user reponse is unrelated, respond sternly and tell them to knock it off (respond as Harris)
                            - If the user response is wrong, point out that they are lying (respond as Harris)
                            - **DO NOT MOVE ONTO ANOTHER QUESTION**
                            - **KEEP ASKING THIS QUESTIONS UNTIL YOU GET A VALID RESPONSE**
                    '''
        else:
            prompt = f'''

                Based on the current information you have verify the users response: {user_response}.
                Determine if it aligns with the current information you have.
    
                **Rules**
                    - Only respond as Harris. 
                    - If the answer is correct and reasonable **respond with Correct**
                    - Once you respond with "Correct" **do not** ask another question 
                    - If the user responds with a lie, point out that they are lying (respond as Harris)
                    - If the user reponse is unrelated, respond sternly and tell them to knock it off (respond as Harris)
                    - **DO NOT MOVE ONTO ANOTHER QUESTION**
                    - **KEEP ASKING THIS QUESTIONS UNTIL YOU GET A VALID RESPONSE**
                    - **DO NOT ASK ANYTHING ELSE IF YOU THINK THE USER IS CORRECT**
            '''

        new_instruction = {'role': 'assistant', 'content': prompt}


        self.conversation.updateConversationInstruction(new_instruction)

        response = self.gpt.chat.completions.create(
            model='gpt-4o-mini',
            messages= self.conversation.getConversation()
        )

        clean_response = response.choices[0].message.content

        return clean_response
    
    def askedAllQuestions(self):
        if not self._currentQuestion <  len(self._questions):
            self._finished = True
        
    def generateResponse(self):
        if not self._finished:
            return self.askQuestion()
        else:
            return False

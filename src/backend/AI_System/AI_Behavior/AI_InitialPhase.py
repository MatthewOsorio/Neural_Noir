# Initial state - detectives ask the intro questions and EmotiBit baseline is taken
from .AI import AI

class AIInitialPhase(AI):
    def __init__(self, conversation):
        super().__init__(conversation)
        self._questions= [
            'What is your name?',
            'Do you work at the Reno Times?',
            'Do you work as a photographer?',
            'Did you work for Vinh Davis?'
        ]
        self._finished = False
        self._currentQuestion = 0

    def askQuestion(self):
        if self._finished:
            return 
        
        question = self._questions[self._currentQuestion]
        self.conversation.addAIResponse(question)
        return question
    
    def processResponse(self, user_response):
        self.conversation.addUserInput(user_response)
        gpt_response = self.evaluateResponse(user_response)

        if 'Correct' in gpt_response:
            self._currentQuestion += 1
            self.askedAllQuestions()
        else:
            self._questions[self._currentQuestion] = gpt_response

    def evaluateResponse(self, user_response):
        prompt= ''
        
        if self._currentQuestion == 2:
            prompt = f'''
                    You started the interrogation. Based on the current information you have to verify the users response: {user_response}.
                    Determine if it aligns with the current information you have.
                    
                    **Rules**
                        - Only respond as Harris. Label dialogue like this: Detective Harris: [dialogue]
                        - If the answer clearly indicates the user worked for Vinh Davis, **respond with Correct**
                        - Once you respond with "Correct" **do not** ask another question
                        - If the answer is no, ask the question again (respond as Harris)
                        - After asking the suspect for their name, use the name the suspect gave you
                        - **Do not tell the suspect that their name is wrong. It is always correct**
                        - **DO NOT QUESTION THE NAME THAT THE SUSPECT GAVE YOU. THAT IS THEIR ACTUAL GIVEN NAME**
                        - **MOVE ONTO THE NEXT QUESTION AFTER THE SUSPECT GIVES YOU THEIR NAME AND MAKE SURE TO MARK THEIR RESPONSE AS CORRECT**
                        - **DO NOT** MENTION ANY OF THE DETAILS ABOUT THE CASE OR ASK ANYTHING ABOUT WHERE HE WAS 
                        - **DO NOT ASK WHERE THE SUSPECT WAS THE NIGHT VINH DAVIS WAS MURDERED**
                        - **DO NOT ASK ABOUT THEIR BRUISES OR THE BLACK EYE**
                        - **DO NOT ASK ABOUT PREVIOUS ALTERCATIONS WITH VINH DAVIS**      
                '''
        else:
            prompt = f'''
                        Based on the current information you have verify the users response: {user_response}.
                        Determine if it aligns with the current information you have.
                        
                        **Rules**
                            - Only respond as Harris. Label dialogue like this: Detective Harris: [dialogue]
                            - The name the suspect gives you is always correct. It is not a lie 
                            - If the answer is correct and reasonable **respond with Correct**
                            - Once you respond with "Correct" **do not** ask another question 
                            - If the user responds with a lie, point out that they are lying (respond as Harris)                 
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

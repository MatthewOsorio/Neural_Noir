# Initial state - detectives ask the intro questions and EmotiBit baseline is taken
from .AI import AI

class AIInitialPhase(AI):
    def __init__(self, conversation):
        super().__init__(conversation)
        self._questions= [
            'What is your name?',
            'Do you work at the Reno Times?',
            'What is your relationship with the Vinh Davis?'
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
                    You started the interrogation. Based on the current information you have verify the users response: {user_response}.
                    Determine if it aligns with the current information you have.
                    
                    **Rules**
                        - If the answer is sufficient with detail **respond with Correct**
                        - Once you respond with "Correct" **do not** ask another question 
                        - If the answer is vague or evasive, point out they are being evasive and ask the question again (respond as Harris)
                        - **Do not** move on to another question until you get an answer with sufficient detail
                        - **DO NOT** MENTION ANY OF THE DETAILS ABOUT THE CASE OR ASK ANYTHING ABOUT WHERE HE WAS 
                        - **DO NOT ASK WHERE THE SUSPECT WAS THE NIGHT VIHN DAVIS WAS MURDRED**

                '''
        else:
            prompt = f'''
                        Based on the current information you have verify the users response: {user_response}.
                        Determine if it aligns with the current information you have.
                        
                        **Rules**
                            - If the answer is correct and reasonable **respond with Correct**
                            - Once you respond with "Correct" **do not** ask another question 
                            - If the user response with a lie, point out that they are lying (respond as Harris)
                            - **Do not ** move on to another question until you get a correct answer
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

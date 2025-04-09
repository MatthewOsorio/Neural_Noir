# Initial state - detectives ask the intro questions and EmotiBit baseline is taken
from .AI import AI
from textwrap import dedent


class AIInitialPhase(AI):
    def __init__(self, conversation):
        super().__init__(conversation)
        self._questions = [
            "[INSTRUCTION] Ask the suspect for what their name is.",
            "[INSTRUCTION] Ask if the suspect worked at Reno Media Company.",
            "[INSTRUCTION] Ask if Mark worked as a photgrapher at Reno Media Company.",
            "[INSTRUCTION] Ask if the Mark worked under Vinh Davis."
        ]
                
        self._finished = False
        self._currentQuestion = 0


    def askQuestion(self):
        gptInput= self._history.getHistory()[:]
        instruction = self._questions[self._currentQuestion]
        gptInput.append({"role": "user", "content": instruction})
        response = self.sendToGPT(gptInput)
        formattedResponse = self.formatResponse(response)
        self._history.addAIResponse(formattedResponse)
        return formattedResponse
    
    def formatResponse(self, response):
        parsedResponse = response.split("\n")
        if '' in parsedResponse: parsedResponse.remove('')

        for index, response in enumerate(parsedResponse):
            newResponse = response.strip()
            parsedResponse[index] = newResponse

        return "\n".join(parsedResponse)

    def processResponse(self, userResponse):
        preppedResponse  = "[MARK] " + userResponse
        self._history.addInstructionOrUserInput(preppedResponse)
        gptResponse = self.evaluateResponse(userResponse)
        self._history.addAIResponse(gptResponse)

        if gptResponse == "Correct":
            print("VALID")
            self._currentQuestion += 1
            self.askedAllQuestions()
        else:
            self._questions[self._currentQuestion] = gptResponse

    def evaluateResponse(self, user_response):
        gptInput= self._history.getHistory()[:]
        instruction= ''

        
        if self._currentQuestion == 3:
            instruction = dedent(f'''
                [INSTRUCTION] Evaluate Mark's response: "{user_response}"
                Your job is to determine if the answer is  and directly addresses the current question.

                **Only do the following:**
                - If Mark clearly states that he worked under Vinh Davis, respond with **Correct** and nothing else.
                - If Mark is lying, dodging the question, or giving vague answers, press harder and **repeat the question**.
                - Do not move to the next question until the response is truthful and clear.
                
                **Rules for this phase:**
                - Both detectives must remain focused on the current question. Do not have them ask different questions. They may reinforce each other, apply pressure, or rephrase the same question, but never change the topic.
                - Do NOT mention any case details (murder, bruises, black eye, arguments, etc.)
                - Do NOT mention Vinh's death or the night it happened.
                - Do NOT ask follow-up questions about location or motives.
                - Do NOT reveal that you know Mark worked under Vinh — make him admit it.
            ''')
        else:
            instruction = dedent(f'''
                [INSTRUCTION] Evaluate Mark's response: "{user_response}"
                Your job is to verify whether Mark is telling the truth based on what you know.

                **Respond with only one of the following:**
                - **Correct** (if the answer is truthful, direct, and sufficient — no explanation needed)
                - Or respond as the detectives pressing harder and re-asking the current question.

                **Important behavior rules:**
                - Both detectives must remain focused on the current question. Do not have them ask different questions. They may reinforce each other, apply pressure, or rephrase the same question, but never change the topic.
                - Do NOT bring up any unrelated details (murder, argument, bruises, etc.)
                - Do NOT move onto another question until the answer is valid and complete.
                - Speak naturally, taking turns between Harris and Miller as needed.
            ''')
        
        gptInput.append({"role": "user", "content": instruction})
        response = self.sendToGPT(gptInput)
        return response
    
    def askedAllQuestions(self):
        if not self._currentQuestion <  len(self._questions):
            self._finished = True
        
    def generateResponse(self):
        if self._finished:
            return False
        else:
            return self.askQuestion()
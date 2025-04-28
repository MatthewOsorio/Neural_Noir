from .AI import AI
from textwrap import dedent

class AIInitialPhase(AI):
    def __init__(self, history, sentimentAnalyzer):
        super().__init__(history, sentimentAnalyzer)
        self._questions = [
            "[INSTRUCTION] Ask the suspect for what their name is. DO NOT MENTION THEIR NAME.",
            #"[INSTRUCTION] Ask if the suspect worked at Reno Media Company.",
            #"[INSTRUCTION] Ask if the suspect worked as a photographer at Reno Media Company.",
            #"[INSTRUCTION] Ask if the suspect worked under Vinh Davis."
        ]
        self._finished = False
        self._currentQuestion = 0
        self._startedInstruction = False

    def askQuestion(self):
        if not self._startedInstruction:
            gptInput = self._aiHistory.getHistory()[:]
            instruction = self._questions[self._currentQuestion]
            gptInput.append({"role": "user", "content": instruction})

            response = self.sendToGPT(gptInput)
            self._startedInstruction = True
            return response
        else:
            return self._questions[self._currentQuestion]

    def processResponse(self, userResponse):
        if self._currentQuestion == 0:
            #Getting players name
            gptResponse = self.evaluateResponse(userResponse)
        else:
            preppedResponse = f"[{self._aiHistory.getPlayerName()}]: " + userResponse
            self._aiHistory.addUserInput(preppedResponse)
            gptResponse = self.evaluateResponse(userResponse)

        if gptResponse == "Correct":
            self._currentQuestion += 1
            self.askedAllQuestions()
            self._startedInstruction = False
        else:
            self._questions[self._currentQuestion] = gptResponse

    def evaluateResponse(self, userResponse):
        playerName = self._aiHistory.getPlayerName()
        gptInput = self._aiHistory.getHistory()[:]
        originalQuestion = self._questions[self._currentQuestion]

        if self._currentQuestion == 0:
            # For getting the players name
            instruction = dedent(f'''
                [INSTRUCTION] You are evaluating the suspect's response to the question: "{originalQuestion}"  
                The suspect's response was: "{userResponse}".

                Your goal is to determine if the suspect has provided a valid NAME.

                **Rules:**
                - A first name alone is also valid.
                - If a valid name is provided (but NOT "Vinh Davis"), return:
                {{"name": "Full name or first name here" }}
                - If no valid name is provided:
                - either Detective Miller or Detective Harris to naturally ask again for the suspect's name.
                - Return the Detective speaking naturally asking for the name again in a string format
                - If the name "Vinh Davis" is provided, treat it as INVALID and mention its the name of the victim in the response.

                **Important Detective Rules:**
                - Only one detective speaks at a time.
                - Stay focused on asking for the suspect's name — do not change the topic.
                - Do not reveal any case details (murder, bruises, arguments, Vinh relationship).
                - Speak naturally and conversationally.
                - Do not include any extra commentary or explanations.
            ''')

            gptInput.append({"role": "user", "content": instruction})

            response = self.sendToGPT(gptInput)

            if isinstance(response, tuple):
                self._aiHistory.updatePlayerName(response[1])
                return response[0]
            else:
                return response
            
        elif self._currentQuestion == 3:
            instruction = dedent(f'''
                [INSTRUCTION] Evaluate {playerName}'s response to the question: "{originalQuestion}"
                His response was: "{userResponse}"

                Your job is to determine if the response is now acceptable and truthful, based on the current message and the prior dialogue.

                **Only do the following:**
                - If {playerName} confirms that he worked under Vinh Davis — even informally or after some resistance — respond with **Correct** and nothing else.
                - Trust the overall intent. If he eventually says something like "Yes", "he was my boss", or "I worked for him", treat it as a valid confirmation — even if he initially dodged.
                - Do not keep repeating the question if he already answered it. Look at the full context, not just this one message.
                - Only repeat the question if his response is still evasive, contradictory, or sarcastic without clarification.

                **Important behavior rules:**
                - Both detectives must remain focused on the current question. Do not have them both ask questions at the same time. They may reinforce each other, apply pressure, or rephrase the same question, but never change the topic.
                - Do NOT change the topic.
                - Do NOT mention any case details (murder, bruises, arguments, etc.)
                - Do NOT reveal that you know {playerName} worked under Vinh — make him admit it.
                - Speak naturally, alternating between Harris and Miller.
            ''')
        else:
            instruction = dedent(f'''
                [INSTRUCTION] Evaluate {playerName}'s response to the question: "{originalQuestion}"
                His response was: "{userResponse}"

                Your job is to verify whether {playerName} is telling the truth based on what you know.

                **Respond with only one of the following:**
                - **Correct** (if the answer is truthful, even if expressed indirectly or creatively — such as “Yes”, “I worked under him”, “He worked for me”, “I did my job under him”, etc.)
                - Or respond as the detectives pressing harder and re-asking the current question.

                **Important behavior rules:**
                - Both detectives must remain focused on the current question. Do not have them both ask questions at the same time. They may reinforce each other, apply pressure, or rephrase the same question, but never change the topic.
                - If you believe {playerName} answers the question truthfully, do not ask follow-up questions.
                - Do NOT bring up any unrelated details (murder, argument, bruises, etc.)
                - Do NOT move onto another question until the answer is valid and complete.
                - Speak naturally, taking turns between Harris and Miller as needed.
            ''')

        gptInput.append({"role": "user", "content": instruction})

        response = self.sendToGPT(gptInput)
        return response

    def askedAllQuestions(self):
        if self._currentQuestion >= len(self._questions):
            self._finished = True

    def generateResponse(self):
        if self._finished: 
            return False
        else:
            return self.askQuestion()
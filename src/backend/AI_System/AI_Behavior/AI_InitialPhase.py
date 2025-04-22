from .AI import AI
from textwrap import dedent

class AIInitialPhase(AI):
    def __init__(self, history):
        super().__init__(history)
        self._questions = [
            "[INSTRUCTION] Ask the suspect for what their name is.",
            "[INSTRUCTION] Ask if the suspect worked at Reno Media Company.",
            "[INSTRUCTION] Ask if Mark worked as a photographer at Reno Media Company.",
            "[INSTRUCTION] Ask if the Mark worked under Vinh Davis."
        ]
        self._finished = False
        self._currentQuestion = 0
        self._startedInstruction = False
        self._currentEvidence = None
        self.currentVerdict = None

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
        preppedResponse = "[MARK]: " + userResponse
        self._aiHistory.addUserInput(preppedResponse)

        gptResponse = self.evaluateResponse(userResponse)

        if gptResponse == "Correct":
            self._currentQuestion += 1
            self.askedAllQuestions()
            self._startedInstruction = False
        else:
            self._questions[self._currentQuestion] = gptResponse

    def evaluateResponse(self, user_response):
        gptInput = self._aiHistory.getHistory()[:]
        originalQuestion = self._questions[self._currentQuestion]
        instruction = ''

        if self._currentQuestion == 3:
            instruction = dedent(f'''
                [INSTRUCTION] Evaluate Mark's response to the question: "{originalQuestion}"
                His response was: "{user_response}"

                Your job is to determine if the response is now acceptable and truthful, based on the current message and the prior dialogue.

                **Only do the following:**
                - If Mark confirms that he worked under Vinh Davis — even informally or after some resistance — respond with **Correct** and nothing else.
                - Trust the overall intent. If he eventually says something like "Yes", "he was my boss", or "I worked for him", treat it as a valid confirmation — even if he initially dodged.
                - Do not keep repeating the question if he already answered it. Look at the full context, not just this one message.
                - Only repeat the question if his response is still evasive, contradictory, or sarcastic without clarification.

                **Important behavior rules:**
                - Both detectives must remain focused on the current question. Do not have them both ask questions at the same time. They may reinforce each other, apply pressure, or rephrase the same question, but never change the topic.
                - Do NOT change the topic.
                - Do NOT mention any case details (murder, bruises, arguments, etc.)
                - Do NOT reveal that you know Mark worked under Vinh — make him admit it.
                - Speak naturally, alternating between Harris and Miller.
            ''')
        else:
            instruction = dedent(f'''
                [INSTRUCTION] Evaluate Mark's response to the question: "{originalQuestion}"
                His response was: "{user_response}"

                Your job is to verify whether Mark is telling the truth based on what you know.

                **Respond with only one of the following:**
                - **Correct** (if the answer is truthful, even if expressed indirectly or creatively — such as “Yes”, “I worked under him”, “He worked for me”, “I did my job under him”, etc.)
                - Or respond as the detectives pressing harder and re-asking the current question.

                **Important behavior rules:**
                - Both detectives must remain focused on the current question. Do not have them both ask questions at the same time. They may reinforce each other, apply pressure, or rephrase the same question, but never change the topic.
                - If you believe Mark answers the question truthfully, do not ask follow-up questions.
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
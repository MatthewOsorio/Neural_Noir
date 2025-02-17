from .AI import AI

class AIInitialPhase(AI):
    def __init__(self, conversation):
        super().__init__(conversation)
        self.setInstructions()

    def setInstructions(self) -> None:
        print("initial")
        self.conversation.updateConversationInstruction({
            'role': 'assistant',
            'content': '''
                You are now starting the interrogation.
                To begin, ask rapport-building questions.

                Create and ask one question at a time in this order:
                    1. Confirm the suspects name is Mark Chadenton
                    2. Confirm the suspect works at the Reno Times
                    3. Ask them about their relationship with the victim.
                    4. Ask what they were doing around 11:30 pm last night.

                Rules:
                - Ask only **one** question at a time and **wait** for the user's response.
                - Do **not** create any response to the question you ask.
                - Do **not** ask the next question until the user responds.
                - If user contradicts or lies do not move one until you have a valid response
                - after you asked all four questions **return FINSIHED**
                ''' 
        })
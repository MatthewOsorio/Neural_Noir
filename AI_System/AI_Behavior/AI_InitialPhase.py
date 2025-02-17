from .AI import AI

class AI_InitialPhase(AI):
    def __init__(self, conversation):
        super().__init__(conversation)
        self.setInstructions()

    def setInstructions(self) -> None:
        self.conversation.updateConversation({
            'role': 'assistant',
            'content': '''
                    You are now starting the interrogation.
                    To begin ask rapport-building questions.

                    Create four questions:
                        1. Ask what the suspect what name is
                        2. Confirm their place of work
                        3. Ask them about their relationship with the victim
                        4. What they were doing around 11:30pm last night

                    Ask each of these quesions one at a time.
                    Once you have asked these question. On the Last Question at "TERMINATE" at the end
                    ''' 
        })




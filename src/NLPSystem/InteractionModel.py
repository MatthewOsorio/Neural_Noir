class IneractionModel:
    def __init__(self):
        self.context='''A murder was commited last night.
                        The victim was the CEO of a company with a reputation of being terrible to his
                        employees and being very unlikeable. He was murdered last night at a company event.
                        When the murder happened, all the lights shut off and there was a loud bang.
                        The murder weapon found was a gun. You're interrogating someone who had a motive
                        and greatly disliked the CEO, and they were at the company event.
                        '''
        self.interaction=[]

    def addToInteraction(self, input) -> None:
        self.interaction.append(input)

    def getLast(self) -> str:
        return self.interaction[-1]["content"]
    
    def getContext(self) -> str:
        return self.context
    
    def getInteraction(self) -> list:
        return self.interaction
    
    def clearInteraction(self) -> None:
        self.interaction.clear()
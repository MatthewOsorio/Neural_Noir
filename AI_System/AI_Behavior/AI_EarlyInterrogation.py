from .AI import AI

class AIEarlyInterrogation(AI):
    def __init__(self, conversation):
        super().__init__(conversation)
        self.setInstructions()

    def setInstructions(self) -> None:
        print("early")
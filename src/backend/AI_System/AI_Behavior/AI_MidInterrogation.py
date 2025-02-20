from .AI import AI

class AIMidInterrogation(AI):
    def __init__(self, conversation):
        super().__init__(conversation)
        self.setInstructions()

    def setInstructions(self):
        print("mid")
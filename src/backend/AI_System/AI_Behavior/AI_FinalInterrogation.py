# Bad-cop scenario
from .AI import AI

class AIFinalInterrogation(AI):
    def __init__(self, conversation):
        super().__init__(conversation)

    def generateResponse(self) -> str:
        pass
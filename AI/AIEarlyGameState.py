from .AIStateInterface import AIStateInterface
from openai import OpenAI

class AIEarlyGameState(AIStateInterface):
    def __init__(self):
        print('first part')

    def generateResponse(self) -> dict:
        print('hello')
        return {}

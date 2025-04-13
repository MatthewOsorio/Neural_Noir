from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from openai import OpenAI
from TTSSystem import TextToSpeechController

if TYPE_CHECKING:
    from AI_Context import AIContext

class AI(ABC):
    def __init__(self, conversation):
        self.gpt = OpenAI()
        self.conversation = conversation
        self.userNervous = None
        self._tts = TextToSpeechController()

    @property
    def behavior(self) -> AIContext:
        return self._behavior
    
    @behavior.setter
    def behavior(self, behavior: AIContext) -> None:
        self._behavior = behavior

    def updateNervous(self, nervousState):
        self.userNervous = nervousState
        
    @abstractmethod
    def generateResponse(self) -> str:
        pass
    
    @abstractmethod
    def processResponse(self, userResponse):
        pass
    
    def getNervous(self):
        return self.userNervous
    
    def formatResponse(self, response):
        lines = [line.strip() for line in response.split("\n") if line.strip()]
        responses = []

        for line in lines:

            if line.startswith("Detective Harris:"):
                speaker = "Harris"
                text = line[len("Detective Harris:"):].strip()
            elif line.startswith("Detective Miller:"):
                speaker = "Miller"
                text = line[len("Detective Miller:"):].strip()
            else:
                raise Exception("UNKNOWN RESPONSE FROM GPT")

            responses.append({"Speaker": speaker, "Text": text})

        return responses

    def sendToGPT(self, prompt):
        gptResponse = self.gpt.chat.completions.create(
            model= 'gpt-4o-mini',
            messages= prompt
        )

        cleanResponse = gptResponse.choices[0].message.content

        detectiveResponses = self.formatResponse(cleanResponse)
        self.makeSpeechFile(detectiveResponses)

        print(detectiveResponses)

    def makeSpeechFile(self, detectiveResponses):
        self._tts.generateTTS(detectiveResponses)

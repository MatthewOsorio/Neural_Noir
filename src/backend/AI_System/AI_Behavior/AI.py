from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from openai import OpenAI

if TYPE_CHECKING:
    from AI_Context import AIContext

class AI(ABC):
    def __init__(self, conversation):
        self.gpt = OpenAI()
        self.conversation = conversation
        self.userNervous = None

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

    def sendToGPT(self, prompt):
        response = self.gpt.chat.completions.create(
            model= 'gpt-4o-mini',
            messages= prompt
        )

        clean_response = response.choices[0].message.content

        return clean_response
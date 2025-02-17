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

    @property
    def behavior(self) -> AIContext:
        return self._behavior
    
    @behavior.setter
    def behavior(self, behavior: AIContext) -> None:
        self._behavior = behavior

    @abstractmethod
    def setInstructions(self) -> None:
        pass

    def generateResponse(self) -> str:
        response = self.gpt.chat.completions.create(
            model='gpt-4o-mini',
            messages= self.conversation.getConversation()
        )

        formattedResponse = response.choices[0].message.content
        return formattedResponse

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from AI.AIBehavior import AIBehavior

class AIStateInterface(ABC):

    @property
    def behavior(self) -> AIBehavior:
        return self._behavior
    
    @behavior.setter
    def behavior(self, behavior: AIBehavior) -> None:
        self._behavior = behavior

    @abstractmethod
    def generateResponse(self) -> dict:
        pass

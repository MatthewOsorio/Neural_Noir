from abc import ABC, abstractmethod

class StyleInterface(ABC):
    #Defining the abstract method that will prompt openAI to generate a response
    @abstractmethod
    def getSystemRole(self) -> dict:
        pass

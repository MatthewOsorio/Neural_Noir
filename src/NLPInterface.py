from abc import ABC, abstractmethod

class NLPInterface(ABC):
    #Defining the abstract method that will prompt openAI to generate a response
    @abstractmethod
    def getSystemRole(self):
        pass

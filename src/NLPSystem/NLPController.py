from openai import OpenAI
from NLPSystem.InteractionModel import IneractionModel as im

class NLPController:

    def __init__(self, style) -> None:
        self.gpt= OpenAI()
        self.style= style
        self.interaction= im()

        #Initalize the system role with the context of the interrogation
        self.context= {"role": "system", "content": self.interaction.getContext()}
        self.interaction.addToInteraction(self.context)

        #Initalize the system role with th passed in style behavior
        self.interaction.addToInteraction(style.getSystemRole())
        #Insert first question
        self.interaction.addToInteraction({"role": "assistant", "content": "Where were you last night?"})

    def addUserInput(self, input) -> None:
        userMessage = {"role": "user", "content": input}
        self.interaction.addToInteraction(userMessage)

    #Can possibly use this to ask for basic info, like how josh said to get the suspect in the habit of saying yes
    def getFirstQuestion(self) -> str:
        return self.interaction.getLast()

    def generateResponse(self) -> str:
        # print(self.style.getStyle())
        response = self.gpt.chat.completions.create(
            model= "gpt-4",
            messages= self.interaction.getInteraction()
        )

        generatedResponse= response.choices[0].message.content
        self.interaction.addToInteraction({"role": "assistant", "content": generatedResponse})

        return generatedResponse

    def changeStyle(self, newStyle) -> None:
        self.style= newStyle
        self.interaction.addToInteraction(self.style.getSystemRole())
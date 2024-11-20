from openai import OpenAI

class NLPController:

    def __init__(self, style, interactionModel):
        self.client= OpenAI()
        self.style= style
        self.interaction= interactionModel

        #Initalize the system role with the context of the interrogation
        self.context= {"role": "system", "content": self.interaction.getContext()}
        self.interaction.addToInteraction(self.context)

        #Initalize the system role with th passed in style behavior
        self.interaction.addToInteraction(style.getSystemRole())
        #Insert first question
        self.interaction.addToInteraction({"role": "assistant", "content": "Where were you last time?"})

    def addUserInput(self, input):
        userMessage= {"role": "user", "content": input}
        self.interaction.addToInteraction(userMessage)
        self.generateResponse()

    def getResponse(self):
        return self.interaction.getLast()

    def generateResponse(self):
        print(self.style.getStyle())
        response = self.client.chat.completions.create(
            model= "gpt-4",
            messages= self.interaction.getInteraction()
        )

        generatedResponse= response.choices[0].message.content
        self.interaction.addToInteraction({"role": "assistant", "content": generatedResponse})

    def changeStyle(self, newStyle):
        self.style= newStyle
        self.interaction.addToInteraction(self.style.getSystemRole())
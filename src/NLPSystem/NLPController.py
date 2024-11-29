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

        #Insert first interrogation question
        #self.interaction.addToInteraction({"role": "assistant", "content": "Where were you last night?"})

    def addUserInput(self, input) -> None:
        userMessage = {"role": "user", 
                       "content": input}
        self.interaction.addToInteraction(userMessage)

    #Can possibly use this to ask for basic info, like how josh said to get the suspect in the habit of saying yes
    def getFirstQuestion(self) -> str:
        firstQuestionResponse = self.gpt.chat.completions.create(
                        model = "gpt-4o",
                        messages = [
                            {
                            "role": "assistant",
                            "content": '''This is an interrogation. Stay in character as an interrogator/detective.
                            To begin, ask rapport-building questions. You don't necessarily have to be friendly.
                            Use the tone of the specified interrogation style. Do not state the style. Stay in character
                            as an interrogator.
                            You can also greet the suspect in the tone of the specified style.
                            Ask them to tell you their name.
                            It is assumed that they live in the United States,
                            and that they work at KingPin Corporation.
                            Use the interrogation style passed in. Ask only two questions in the same sentence:
                            their name and a question that will get the suspect to say "yes". You can refer to
                            the suspect by the name they provide throughout interrogation.
                            '''
                            },
                        ],
        )
        firstQuestion = firstQuestionResponse.choices[0].message.content
        self.interaction.addToInteraction({"role": "assistant",
                                          "content": firstQuestion})
        return self.interaction.getLast()

    def generateResponse(self) -> str:
        # print(self.style.getStyle())
        response = self.gpt.chat.completions.create(
            model= "gpt-4o",
            messages= self.interaction.getInteraction()
        )

        generatedResponse= response.choices[0].message.content
        self.interaction.addToInteraction({"role": "assistant",
                                           "content": generatedResponse})

        return generatedResponse

    def changeStyle(self, newStyle) -> None:
        self.style= newStyle
        self.interaction.addToInteraction(self.style.getSystemRole())
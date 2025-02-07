from openai import OpenAI
from ConversationModel import ConversationModel

class AI:
    def __init__(self):
        self.gpt = OpenAI()
        self.conversation= ConversationModel()

    def getFirstQuestions(self):
        self.conversation.updateConversation({
                'role': 'assistant',
                'content': '''
                            You are now starting the interrogation.
                            To begin ask rapport-building questions.

                            Create four questions:
                                1. Ask what the suspect what name is
                                2. Confirm their place of work
                                3. Ask them about their relationship with the victim
                                4. What they were doing around 11:30pm last night
                            
                            Format the questions this way:
                                1. question one
                                2. question two
                                3. question three
                                4. question three
                            '''  
        })

        response= self.gpt.chat.completions.create(
            model='gpt-4o-mini',
            messages= self.conversation.getConversation()
        )
    
        firstQuestions = response.choices[0].message.content
        print(firstQuestions)
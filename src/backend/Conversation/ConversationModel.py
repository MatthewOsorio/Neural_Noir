class ConversationModel:

    conversation=[]

    def __init__(self, database, sessionController):
        self._database = database
        self._sessionController = sessionController
        ConversationModel.conversation.append(ConversationModel.context)

    def sendUserResponseToDB(self, startTime, endTime, userResponse, npcResponse):
        sessionID = self._sessionController.getSessionID()
        feedback_ID = None
        print(f"Logging to DB: SessionID={sessionID}, UserInput={userResponse}")  # Debug
        try:
            self._database.insertInteraction(startTime, endTime, userResponse, npcResponse, sessionID, feedback_ID)
        except Exception as e:
            print(f"Cannot insert user response into DB: {e}")

    # def addAIResponse(self, ai_response) -> None:
    #     ConversationModel.conversation.append({'role': 'assistant', 'content': ai_response})

    # def addUserInput(self, new_input) -> None:
    #     ConversationModel.conversation.append({'role': 'user', 'content': new_input})

    def getConversation(self) -> list:
        return ConversationModel.conversation 
    
    def getContext(self):
        return ConversationModel.context
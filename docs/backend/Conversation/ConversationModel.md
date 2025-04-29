# ConversationModel Class
This class stores the converesation in the form of a list of dictionaries.

## ConversationModel() -> None
This method appends the system directions fo gpt at the beginning of the list. That way the gpt global instructions are set.

## sendUserReponseToDB(startTime, endTime, response) -> None
This method sends the users response and when the users said it to the SQLite database.

## addAIResponse(aiResopnse) -> None
This method formats the ai responses and adds it to the conversation list

## addUserInput(newInput) -> None
This method formates the user reponse and adds it to the conversation list

## getConversation() -> list
This method returns the list representing the conversation

## getContext() -> dict
This method returns the system instructions for gpt.
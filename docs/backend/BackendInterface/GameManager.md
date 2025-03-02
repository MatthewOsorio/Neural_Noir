# GameManager Class
This class acts as the interface between the frontend and backend. This class creates all the objects necessary to run the game and coordinates the communication between the classes.

## GameManager() -> None
This class has variables that stores references of all the object the game needs to functions

## setupGame(emotibitUsed) -> None
This method instantiates the objects necessary to run the game, it determines which objects to instantiate depending on whether or not the emotibit is being used.

## generateAIResponse() -> str
This method invokes the generateResponse method in the AI Controller and returns the generated AI response

## listenToUser() -> None
This method invokes listen and transcribe methods in speech recongition object to collect user speech and transcribes it to a string so the users response can be processed by the AI controller. In addition it also send it to the database by invoking the sendUserResponseTODB method in the ConversationModel object.

## processUserResponse(userResponse) -> None
This method invokes the processUserResponse from the AI Controller.

## updateGameState(state) -> None
This method invokes the updateState method from the Game State Manager object with the new state.

## getUserHeartRate() -> float
This method returns the heart rate from the BiometricController by invoking the getHeartRate method.
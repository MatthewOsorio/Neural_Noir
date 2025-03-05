# GameManager Class
This class acts as the interface between the frontend and backend. This class creates all the objects necessary to run the game and coordinates the communication between the classes.

## Work flow of class
This is the general workflow of the class and how this class works with the AI system. The AI System uses the <a href= 'https://www.geeksforgeeks.org/state-design-pattern/'>state design pattern</a>. This means that depending on whatever AI phase is active the methods generateAIResponse and processeUserResponse will behave differently because AI phase has thier own implemention of these methods. The AI phase will automatically be set when you update the game state via the updateGameState method. The first thing you have to is set the game state, then call genrateAIResponse which will return the question the AI wants to ask, then invoke listenToUser method to transcribe what the user is saying then it will send it will invoke the correct method for the AI to process the user response. 

updateGameState(int) &#x2192; generateAIResponse() &#x2192; listenToUser &#x2192; repeat last two methods until generateAIResponse() returns False indicating it has finsihed asking question &#x2192; restart cycle

## GameManager() -> None
This class has variables that stores references of all the object the game needs to functions.

## setupGame(emotibitUsed) -> None
This method instantiates the objects necessary to run the game, it determines if the biometric related classes need to be instantiated if the emotibit is being used. **IF THE EMOTIBIT IS NOT BEING USED THE THOSE CLASSES SHOULD NOT BE INSTANTIATED.**

## generateAIResponse() -> str
This method invokes the generateResponse method in the AI Controller that has the current AI phase and returns the generated AI response.

## listenToUser() -> None
This method invokes listen and transcribe methods in speech recongition object to collect user speech and transcribes it to a string &#x2192; then it will invoke the processUserResponse with the transcribed string. In addition it also send it to the database by invoking the sendUserResponseTODB method in the ConversationModel object.

## processUserResponse(userResponse) -> None
This method invokes the processUserResponse from the AI Controller.

## updateGameState(state) -> None
This method invokes the updateState method from the Game State Manager object with the new state. Automatically the AI phase and biometrci controller (if being used) will update.

## getUserHeartRate() -> float
This method returns the heart rate from the BiometricController by invoking the getHeartRate method.
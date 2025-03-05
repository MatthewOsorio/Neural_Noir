# AIController Class
This class acts as the manager of the AI system. Here we set and store the AI phase that correlates to the current state of the game and contains the necessary functions for the AI phases to work. 

## Work flow of class
The AI phase gets set when the update method gets invoked, which gets invoked in the updateState method from the GameStateManager class. So when the game state updates the proper AI phase will be set automatically. So now when you call the generateResponse and processUserResponse in this class you will get responses that are from this phase.  

## AIController (conversation) -> None
This class holds a reference to the current AI behavior, a reference to the conversation model to have access to the convsersation history for GPT, and a variable to keep track of the user state if the Emotitbit is being used.

## setAIBehavior(state) -> None
This methods gets called in the update method. Depending on the new state of the game the corresponding AI behevaior will be set in the ai variable.

## update(state) -> None
This method gets called in the GameStateManager class when the notifyAIReference gets invoked, it gets invoked when you update the interal state of the game. This is done so the AI controller can be updated with the new game state.

## generateResponse() -> str
This method invokes the generateResponse method from the current AI phase that is stored in the ai reference variable and returns the AI generated response.

## processUserResponse(userResponse) -> None
This method invokes the generateResponse method of the current AI phase that is stored in the ai reference variable. 

## updateNervous(isNervous) -> None
This method updates the userNervous variable which stores the current state of the user. This method is invoked in the setNervous method in the Biometric Controller. When the Biometric Controller updates the nervous state of the user the AI will be notified and make adjustments on tht prompt, **IF THE EMOTIBIT IS BEING USED**

# AIController Class
This class acts as manager of the AI system. Depending on the state of the game, the AI controller will update the behavior of the AI to the corresponding state. 


## AIController (conversation) -> None
This class holds a reference to the current AI behavior, a reference to the conversation model to have access to the convsersation history for GPT, and a variable to keep track of the user state. If the emotibit is being used the user state will influence the AI responses.

## setAIBehavior(state) -> None
This methods gets called in the update method. Depending on the new state of the game the corresponding AI behevaior will be set.

## update(state) -> None
This method gets called when the game state manager invokes the notifyAIReference method when the internal game state updates. This is done so the AI controller can updat the current AI behavior automatically when game state updates.

## generateResponse() -> str
This method invokes the generateResponse method of the current AI Behavior that is stored in the ai reference variable and returns the AI generated response.

## processUserResponse(userResponse) -> None
This method invokes the generateResponse method of the current AI Behavior that is stored in the ai reference variable. 

## updateNervous(isNervous) -> None
This method updates the userNervous variable which stores the current state of the user. This method is invoked in the setNervous method in the Biometric Controller.

# GameStateManager Class
This class acts as a manager for the state of the game. This class is responsible for updating the game state, notifying the AI system and Biometric system (**IF THE EMOTIBIT IS BEING USED**), and returning the current state of the game.

## GameStateManager() -> None
This class holds a attribute that stores the current state of the the game, a boolean of whether or not the emotibit is being used, a list storying the history of the states, a reference to the 
AI Controller, and a reference to the Biometric Contoller.

## setAIReference(aiReference) -> None
This method sets the ai reference so the AI system can be notified when the game state updates in this class.

## setBiometricReference(biometricReference) -> None
This method sets the biometric reference so the Biometric system can be notified when the game state updates in this class **IF THE EMOTIBIT IS BEING USED**.

## notifyAIReference() -> None
This method gets invoked in the updateState method in this class. This is done so when the game state updates the AI phase will also update automatically by invoking the update method that belongs in the AI refernce.

## notifyBiometricReference() -> None
This method invokes the update method from the biometric reference. This method is so the Biometric Controller knows the internal game state has changed and so it can transition from determining the baseline to monitoring. **IF THE EMOTIBIT IS BEING USED**

## updateState(state) -> None
This method updates the internal state of the game based on the Game State defined in the GameState class. When it intenral game state updates the ai and biometric reference gets notified(**IF THE EMOTIBTI IS BEING USED**).

## getCurrentState() -> GameState
This method returns the current internal state of the game.

## getEmotibitUsed() -> bool
This methods returns the value in the emotibitUsed attribute.

## setEmotibitUsed(isUsed) -> None
This method sets the emotibitUsed attribute to true or false.
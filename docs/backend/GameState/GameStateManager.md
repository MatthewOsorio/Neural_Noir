# GameStateManager Class
This class acts as a manager for the state of the game.

## GameStateManager() -> None
This class holds a variable that stores the current state of the the game, a boolean of whether or not the emotibit is being used, a list storying the history of the states, a reference to the 
AI Controller, and a reference to the Biometric Contoller.

## setAIReference(aiReference) -> None
This method sets the ai reference for the class object.

## setBiometricReference(biometricReference) -> None
This method sets the biometric reference for the class object.

## notifyAIReference() -> None
This method invokes the update method from the ai reference. This method is so the AI controller knows the internal game state has changed and to update the AI behavior.

## notifyBiometricReference() -> None
This method invokes the update method from the biometric reference. This method is so the Biometric Controller knows the internal game state has changed and so it can transition from determining the baseline to monitoring. 

## updateState(state) -> None
This method updates the internal state of the game based on the Game State defined in the GameState class. When it intenral game state updates the ai and biometric reference gets notified.

## getCurrentState() -> GameState
This method returns the current internal state of the game.

## getEmotibitUsed() -> bool
This methods returns the value in the emotibitUsed class variable.

## setEmotibitUsed(isUsed) -> None
This method sets the emotibitUsed class variable.
# AIContext Class
This class is the context manager for the AI phases. Necessary for the <a href= 'https://www.geeksforgeeks.org/state-design-pattern/'>state design pattern</a> to applied to this system. It stores the current AI phases and invokes the methods in those phases.

# AIContext(state) -> None
This class has a class variable that holds a reference to the current AI phase by invoking the setAIBehavior with the current state.

# setAIBehavoir(state) -> None
This method sets the current AI phase and sets the reference to the AIContext manager in the AI abstract base class.

# processUserResponse(userResponse) -> None
This method invokes the processResponse method in the current AI phase that is stored in the state class variable.

# generateReponse() -> str
This method invokes the generateReponse method in the current AI behavior that is stored in the state class variable and returns the response.
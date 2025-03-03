# AIContext Class
This class is the manager for the AI Behaviors. Necessary for the state design pattern applied to this system. 

# AIContext(state) -> None
This class has a class variable that holds a reference to the current AI behavoir and invokes the setAIBehavoir method

# setAIBehavoir(state) -> None
This method sets the current AI Behavoir and sets the reference to the AI context manager in the AI abstract base class.

# processUserResponse(userResponse) -> None
This method invokes the processResponse method in the current AI behavoir that is stored in the state class variable.

# generateReponse() -> str
This method invokes the generateReponse method in the current AI behavior that is stored in the state class variable and returns the response.
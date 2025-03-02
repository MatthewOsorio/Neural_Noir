# AI Class
This class is an abstract base class that enforces the different AI behavoir to implement thier own versions of certain methods and share access to certain methods.

## AI(conversation) -> None
This method defines a reference to the OpenAI object send requests to ChatGPT to genenrate AI responses, holds a reference to the conversation object that stores the current conversation, and holdes has a variable that is stores the current nervous state of the user.

## behavoir() -> AIContext
This method returns the current AIContext object. 

## behavior(behavior) -> None
This method sets the refernece to current AIContext.

## updateNervous(nervousState) -> None
This method updates variable that stores the current nervous state of the user with the new user nervous state

## generateResponse() -> str
This is an abstract method that needs to be implemented in the children classes
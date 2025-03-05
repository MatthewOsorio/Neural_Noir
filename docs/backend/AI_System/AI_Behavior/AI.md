# AI Class
This class is an abstract base class that enforces the different AI phases to implement thier own versions of certain methods and for all the different AI phases to share certain methods and attributes.

## AI(conversation) -> None
This method defines a reference to the OpenAI object send requests to ChatGPT to genenrate AI responses, holds a reference to the conversation object that stores the current conversation, and holdes has a variable that is stores the current nervous state of the user. All the AI phases have access to these attributes. 

## behavoir() -> AIContext
This method returns the current AIContext object. The AIContext is is the context manager for the different AI phases, the AI system implements the <a href= 'https://www.geeksforgeeks.org/state-design-pattern/'>state design pattern</a>.

## behavior(behavior) -> None
This method sets the refernece to current AIContext. The AIContext is is the context manager for the different AI phases, the AI system implements the <a href= 'https://www.geeksforgeeks.org/state-design-pattern/'>state design pattern</a>.

## updateNervous(nervousState) -> None
This method updates the attribute that stores the current nervous state of the user with the new user nervous state. This method gets invoked when the AIController invokes this method in the updateNervous method that belongs in the AIController class.

## generateResponse() -> str
This is an abstract method that needs to be implemented in the children classes.

## processReponse(userRespose) -> None
This is an abstract method that needs to be implemented in the children classes.

## getNervous() -> bool
This methods returns the current nervous state of the user that is stored in the userNervous attribute.

## sendToGPT(prompt) -> str:
This method makes an api call to gpt with the passed in prompt and returns the response.
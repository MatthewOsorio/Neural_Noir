# AIInitalPhase Class
This class defines how the AI behaves in the initial phase of the game. This class inherits from the AI abstract base class.

## AIInitialPhase(conversation) -> None
This class holds a reference to the conversation model that is stored in the parent class, a list of the questions the AI has to ask in this part of the game, a finished variable that stores a boolean depending if all the questions have been asked, a variable called current that keeps track fo the index of the current questions that is being asked. 

## askQuestion() -> str
If all the haven't been asked, it will return the question to ask the user

## processResponse(userResponse) -> str
This method stores the user input into the conversation model, and invokes the evaluateResponse method of this class. If the evaluateResponse method returns 'Correct' the next question will be asked, otherwise an AI response will be returned and set as current question to ask.

## evaluateResponse(userResponse) ->  str
This method evaluates the user response to the question begin asked, if gpt deems the response to be correct, 'Correct' will be returned. Otherwise gpt will generate a response to the incorrect statement and that response will be returned

## askedAllQuestion() -> None
This method checks if all the questions in the list have been asked, if they have been the finsihed variable stored in the class will be set to true, preventing any other questions to be asked.

## generateResponse() -> str/bool
If all the questions haven't been asked this method will return the current question, otherwise false will be returned.
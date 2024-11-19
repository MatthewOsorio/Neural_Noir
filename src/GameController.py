from openai import OpenAI

class GameController:
    #Constructor for GameController only takes a speech recognition object, biometric logic object, and database object. The rest of the attributes will be set in the other methods
    def __init__(self, speechRecognition, biometricLogic, database):
        self.__client= OpenAI()
        self.__sr= speechRecognition
        self.__bLogic= biometricLogic
        self.__database= database
        self.__responseStyle= None
        self.__discrepancy= None
        self.__response= None

    #Ask openAI to analyze the userIput to deteremine if there is a discrepancy, if there is set the discrepancy flag to true, if there is not set it to false
    def analyzeInput(self):
        pass
    
    #Call the prompt() method within the current NLPInterface, pass in the speech input, and the openAI object. Obtain the speech input by calling the getter from the sr attribute
    def generateResponse(self):
        pass 

    #Getter for generated response
    def getResponse(self):
        return self.__response

    #Setter for the responseStyle
    def setNLPInterface(self, NLPInterface): 
        self.__responseStyle= NLPInterface

    #This method calls the insert() methods from the database object this class has a reference to. The insert() methods takes in the start and end time, discrepancy, the user input, and the response
    def sendToDB(self):
        pass


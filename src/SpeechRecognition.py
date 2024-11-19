import speech_recognition as sr

class SpeechRecognition:
    #Construtor for speech recognition, it does not take anything
    def __init__(self):
        self.__listener= sr
        self.__userInput= None
        self.__startTime= None
        self.__endTime= None

    #Recieve user input and transcribe it into a string, it then gets stored into the userInput attribute
    def listen(self):
        pass
    
    #Getter for user input
    def getUserInput(self):
        return self.__userInput

    #Setter for start time
    def setStartTime(self, time):
        self.__startTime= time

    #Getter for start time
    def getStartTime(self):
        return self.__startTime
    
    #Setter for end time
    def setEndTime(self, time):
        self.__endTime= time

    #Getter for end time
    def getEndTime(self):
        return self.__endTime
    

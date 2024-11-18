class EmotibitReader:
    #construtor for emotibitreader, only takes in database object, logic object, and filename. The rest of the attributes will be set within the methods in the class
    def __init__(self, database, logic, filename):
        self.__database= database
        self.__logic= logic
        self.__filename= filename
        self.__startTime= -1.0
        self.__endTime= -1.0
        self.__temperature=  -1.0
        self.__heartRate= -1
        self.__skinConduction= -1.0
    
    #This methods is supposed to utlize the brianflow sdk to collect data from emotibit and write it to the file
    def readData(self):
        pass

    #This methods is supposed to read the file where the biometric values are written to and set the biometric values from it. Maybe we can find the average of each values and use those?
    def setBiometricValues(self):
        pass

    #This method is take the biometric values and times stored in the attributes and send them to the database by using the insert() method inside the database object. This should be called inside the setBiometricValues() method towards the end
    def sendToDB(self):
        pass
    
    #This methods is call the isSuspicious() methods from the logic object and pass the biometric values into it. I also suggest we call this method inside the setBiometricValues() methods towards the end
    def compareValues(self):
        pass

    #Getter for filename
    @property
    def filename(self):
        return self.__filename
    
    #Setter for filename
    @filename.setter
    def filename(self, filename):
        self.__filename= filename

    #Getter for start time
    @property
    def startTime(self):
        return self.__startTime
    
    #Setter for start time
    @startTime.setter
    def startTime(self, time):
        self.__startTime= time

    #Getter for end time
    @property
    def endTime(self):
        return self.__endTime
    
    #Setter for end time
    @endTime.setter
    def endTime(self, time):
        self.__endTime= time
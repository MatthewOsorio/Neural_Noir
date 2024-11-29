from SessionController import SessionController as sc

class GameController:
    def __init__(self, speechToText, nlpController, ttsController, database):
        self.stt = speechToText
        self.nlp = nlpController
        self.tts = ttsController
        self.database= database
        self.session= sc(self.database)
        self.tempUserInput= None
        self.tempGeneratedResponse= None

    def convertSpeechToText(self):
        processed_audio_input = self.stt.listen()
        transcription = self.stt.transcribe(processed_audio_input)
        return transcription

    def speechInput(self):
        input = self.convertSpeechToText()
        self.nlp.addUserInput(input)
        self.tempUserInput= input
        self.sendInteractionTODB()
        return input

    def createDetectiveResponse(self):
        response= self.nlp.generateResponse()
        self.convertTextToSpeech(response)
        self.tempGeneratedResponse = response
        return response

    def convertTextToSpeech(self, response):
        self.tts.generateTTS(response)
        
    def startSession(self): 
        self.session.start()

    def startInterrogation(self):
        self.startSession()
        firstQ = self.nlp.getFirstQuestion()
        print(firstQ)
        self.convertTextToSpeech(firstQ)
        self.tempGeneratedResponse= firstQ

    def sendInteractionTODB(self):
        self.database.insertInteraction(self.stt.getStartTime(), self.stt.getEndTime(), self.tempUserInput, self.tempGeneratedResponse, self.session.getSessionID())

    def getConversationFromDB(self):
        conversation =self.database.fetchConversation(self.session.getSessionID())
        return conversation
    

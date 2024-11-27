import SessionController as sc

class GameController:
    def __init__(self, nlpController, ttsController, dbController):
        self.nlp= nlpController
        self.tts= ttsController
        self.session= sc.SessionController(dbController)

    def convertSpeechToText(self):
        processed_audio_input = self.stt.listen()
        transcription = self.stt.transcribe(processed_audio_input)
        return transcription

    def speechInput(self):
        input = self.convertSpeechToText()
        self.nlp.addUserInput(input)
        return input

    def createDetectiveResponse(self):
        response= self.nlp.generateResponse()
        self.convertTextToSpeech(response)
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
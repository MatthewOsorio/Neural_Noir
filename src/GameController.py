class GameController:
    def __init__(self, nlpController, ttsController):
        self.nlp= nlpController
        self.tts= ttsController

    def speechInput(self, input):
        self.nlp.addUserInput(input)
    
    def createDetectiveResponse(self):
        response= self.nlp.generateResponse()
        self.convertTextToSpeech(response)
        return response

    def convertTextToSpeech(self, response):
        self.tts.generateTTS(response)

    def startInterrogation(self):
        firstQ = self.nlp.getFirstQuestion()
        print(firstQ)
        self.convertTextToSpeech(firstQ)
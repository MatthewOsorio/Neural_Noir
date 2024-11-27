class GameController:
    def __init__(self, speechToText, nlpController, ttsController):
        self.stt = speechToText
        self.nlp = nlpController
        self.tts = ttsController

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

    def startInterrogation(self):
        firstQ = self.nlp.getFirstQuestion()
        print(firstQ)
        self.convertTextToSpeech(firstQ)
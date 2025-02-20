from openai import OpenAI
import speech_recognition as sr
from datetime import datetime

class SpeechToText:
    def __init__(self):
        self.gpt = OpenAI()
        self.recognizer = sr.Recognizer()
        self.startTime = None
        self.endTime = None

    def listen(self):
        # Increase the time to from end of audio input to processing
        # self.recognizer.pause_threshold = 3.0
        now = datetime.now()
        self.startTime = now.strftime("%H:%M:%S")

        with sr.Microphone() as source:
            audio = self.recognizer.listen(source)
        return audio

    def transcribe(self, processed_audio):
        try:
            transcription = self.recognizer.recognize_whisper_api(processed_audio)
            now = datetime.now()
            self.endTime = now.strftime("%H:%M:%S")
            return transcription
        except:
            now = datetime.now()
            self.endTime = now.strftime("%H:%M:%S")
            return None

    def getStartTime(self):
        return self.startTime
    
    def getEndTime(self):
        return self.endTime
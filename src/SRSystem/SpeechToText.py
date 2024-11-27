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
        self.startTime = datetime.now()
        with sr.Microphone() as source:
            audio = self.recognizer.listen(source)
        return audio

    def transcribe(self, processed_audio):
        try:
            transcription = self.recognizer.recognize_whisper_api(processed_audio)
            self.endTime = datetime.now()
            return transcription
        except:
            self.endTime = datetime.now()
            return None

''' 
# Output Testing  
speech = SpeechToText()
processed_audio_input = speech.listen()
print(f"start time: {speech.startTime}")
transcription = speech.transcribe(processed_audio_input)
print(transcription)
print(f"end time: {speech.endTime}")
'''   
from openai import OpenAI
from pathlib import Path
from tempfile import NamedTemporaryFile
from TTSSystem.AudioComponent import AudioController as ac

class TextToSpeechController:
    def __init__(self):
        self.gpt = OpenAI()
        self.audio= ac()

    def generateTTS(self, response):
        tts = self.gpt.audio.speech.create(
            model='tts-1',
            voice='onyx',
            response_format= "mp3",
            input= response,
        )

        self.saveTTSToFile(tts)

    def saveTTSToFile(self, tts):
        with NamedTemporaryFile(delete= False, suffix=".mp3") as f:
            temppath= Path(f.name)
            f.close()

        tts.write_to_file(temppath)
        self.speak(temppath)

    def speak(self, filepath):
        self.audio.playText(filepath)
        #print(filepath.exists())
        filepath.unlink()
        #print(filepath.exists())

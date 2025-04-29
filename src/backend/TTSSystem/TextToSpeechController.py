from openai import OpenAI
from pathlib import Path
from tempfile import NamedTemporaryFile
import threading
from .AudioController import AudioController as ac

class TextToSpeechController:
    def __init__(self):
        self.gpt = OpenAI()
        self.audio= ac()
        self._voices = {
            "Harris": 'ash',
            "Miller": 'onyx'
        }

    def generateTTS(self, responses):
        threads = []

        for index, response in enumerate(responses):
            thread = threading.Thread(target= self.ttsTask, args=(index, response["Speaker"], response["Text"], responses))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    def ttsTask(self, index, speaker, text, responses):
        speaker = speaker.replace("Detective ", "").strip()
        voice = self._voices.get(speaker)
        
        tts = self.gpt.audio.speech.create(
            model="tts-1",
            voice=voice,
            response_format="mp3",
            input=text
        )

        with NamedTemporaryFile(delete= False, suffix=".mp3") as f:
            temppath = Path(f.name)
            f.close()

        tts.write_to_file(temppath)

        responses[index]["AudioFilepath"] = temppath
        
    def speak(self, filepath):
        self.audio.playText(filepath)
        #print(filepath.exists())
        #print("Not busy")
        filepath.unlink()
        #print(filepath.exists())


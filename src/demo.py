import GameController as gc
from NLPSystem.NLPController import NLPController as nlp
from NLPSystem.IntimidatingStyle import IntimidatingSytle
from NLPSystem.InteractionModel import IneractionModel
from TTSSystem.TextToSpeechController import TextToSpeechController as ttsc
from SRSystem.SpeechToText import SpeechToText as stt
from DatabaseController import DatabaseController as db

newInteraction = IneractionModel()
intimidating = IntimidatingSytle()
nlpController = nlp(intimidating)
game = gc.GameController(stt(), nlpController, ttsc(), db())

game.startInterrogation()


while True:
    speech = game.speechInput()
    print(f"< {speech}")
    print(game.createDetectiveResponse())

    

    
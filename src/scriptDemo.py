import GameController as gc
from NLPSystem.NLPController import NLPController as nlp
from NLPSystem.IntimidatingStyle import IntimidatingSytle
from TTSSystem.TextToSpeechController import TextToSpeechController as ttsc
from SRSystem.SpeechToText import SpeechToText as stt
from DatabaseController import DatabaseController as db
from ScriptDisplay import ScriptDisplay

intimidating = IntimidatingSytle()
nlpController = nlp(intimidating)
game = gc.GameController(stt(), nlpController, ttsc(), db())

test = ScriptDisplay(game)

# game.startInterrogation()


# while True:
#     speech = game.speechInput()
#     print(f"< {speech}")
#     print(game.createDetectiveResponse())
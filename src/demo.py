import GameController as gc
from NLPSystem.NLPController import NLPController as nlp
from NLPSystem.IntimidatingStyle import IntimidatingSytle
from TTSSystem.TextToSpeechController import TextToSpeechController as ttsc


intimidating = IntimidatingSytle()
nlpController = nlp(intimidating)
game = gc.GameController(nlpController, ttsc())

game.startInterrogation()

while True:
    game.speechInput(input("> "))
    print(game.createDetectiveResponse())
# #Only for testing sake, can be deleted after
# import SpeechRecognition
# import GameController
# import ProfessionalStyle
# import NLPInterface

# sr= SpeechRecognition.SpeechRecognition()
# sr.setUserInput("You're not getting anything out of me dummy!") 

# gc= GameController.GameController(sr, "null", "null")
# gc.setNLPInterface(ProfessionalStyle.ProfessionalStyle())

# gc.generateResponse() 
import ProfessionalStyle as ps
import NLPController as nc
import InteractionModel as im

test= nc.NLPController(ps.ProfessionalStyle(), im.IneractionModel())

while True:
    print(test.getResponse())
    test.addUserInput(input("> "))
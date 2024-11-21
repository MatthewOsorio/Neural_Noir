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
import FriendlyStyle as fs
import IntimidatingStyle as IS

professional = ps.ProfessionalStyle()
friendly= fs.FriendlySytle()
intimidating= IS.IntimidatingSytle()

test= nc.NLPController(professional, im.IneractionModel())
print(test.getFirstQuestion())

counter=1
while True:

    test.addUserInput(input("> "))
    print(test.generateResponse())

    counter += 1
    if(counter % 3 == 1):
        test.changeStyle(professional)
    elif (counter % 3 == 2):
        test.changeStyle(friendly)
    elif (counter % 3 == 0):
        test.changeStyle(intimidating)

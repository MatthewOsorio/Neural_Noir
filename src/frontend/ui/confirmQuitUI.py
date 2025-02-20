from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectGui import DirectFrame, DirectLabel, DirectButton
import sys

#Moved to menu.py

from menu import mainMenu

class confirmQuit:

    def __init__(self, base):
        self.base = base

        self.generateBackground()
        self.createContents()
        self.hide()
    
        self.mainMenu = mainMenu(self)

    def generateBackground(self):
        self.backgroundImage= OnscreenImage(image='images/Room_Backdrop_Blur.png',
                                            pos=(0, 0, 0,),
                                            parent=self.base.render2d)
    
    def createContents(self):
        self.parentFrame = DirectFrame(frameColor=(0, 0, 0, 0),
                            frameSize=(-0.75, 0.75, -0.75, 0.75),
                            pos= (0, 0, 0),
                            parent=self.base.aspect2d)
        
        titleText= 'Are you sure?'
        #TitleFrame= DirectFrame(parent= parentFrame,
                                #frameColor= (0, 0, 0, 0),
                                #frameSize= (-0.50, 0.50, -0.25, 0.25),
                                #pos= (0, 0, 0.5))
        
        self.titleTextFrame= DirectLabel(parent= self.parentFrame,
                                    text= titleText,
                                    text_scale= (0.1, 0.1),
                                    text_fg= (255, 255, 255, 0.9),
                                    frameColor= (0, 0, 0, 0),
                                    pos = (0,0.5,0.5))
        
        self.yesButtom= DirectButton(parent= self.parentFrame,
                                text="Yes",
                                scale= 0.075,
                                pos= (-0.40, 0, 0),
                                command = sys.exit)
        
        self.noButtom= DirectButton(parent= self.parentFrame,
                        text="No",
                        scale= 0.075,
                        pos= (0.40, 0, 0))
        
               
    def hide(self):
        self.parentFrame.hide()

    def show(self):
        self.parentFrame.show()
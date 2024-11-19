from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectGui import DirectFrame, DirectLabel, DirectButton

class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        self.generateBackground()
        self.createContents()

    def generateBackground(self):
        self.backgroundImage= OnscreenImage(image='../images/Room_Backdrop_Blur.png',
                                            pos=(0, 0, 0,),
                                            parent=self.render2d)
    
    def createContents(self):
        parentFrame = DirectFrame(frameColor=(0, 0, 0, 0),
                            frameSize=(-0.75, 0.75, -0.75, 0.75),
                            pos= (0, 0, 0))
        
        titleText= 'Are you sure?'
        TitleFrame= DirectFrame(parent= parentFrame,
                                frameColor= (0, 0, 0, 0),
                                frameSize= (-0.50, 0.50, -0.25, 0.25),
                                pos= (0, 0, 0.5))
        
        titleTextFrame= DirectLabel(parent= TitleFrame,
                                    text= titleText,
                                    text_scale= (0.1, 0.1),
                                    text_fg= (255, 255, 255, 0.9),
                                    frameColor= (0, 0, 0, 0))
        
        yesButtom= DirectButton(parent= parentFrame,
                                text="Yes",
                                scale= 0.075,
                                pos= (-0.40, 0, 0))
        
        noButtom= DirectButton(parent= parentFrame,
                        text="No",
                        scale= 0.075,
                        pos= (0.40, 0, 0))
        
app= MyApp()
app.run()
from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectLabel import DirectLabel
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectScrolledFrame import DirectScrolledFrame
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectGui import DGG
from panda3d.core import TextNode
from panda3d.core import TransparencyAttrib

class ScriptDisplay():
    def __init__(self, manager, gameManager, pauseMenu):
        self.manager = manager
        self.gameManager = gameManager
        self.pauseMenu = pauseMenu
        self.generateDisplayBox()
        print("ScriptDisplay intialized") # debug

    def formatScript(self, conversation):
        script = []

        for interaction in conversation:
            interactionString = f"{interaction[0]}: {interaction[1]}\n"
            script.append(interactionString)
            

        return script
    
    def getScript(self):
        print("Getting script")
        sessionID = self.gameManager._sessionController.getSessionID()
        conversation = self.gameManager._database.fetchConversation(sessionID)

        #print("Fetched conversation from DB: ", conversation) # debug
        script = self.formatScript(conversation)
      #  print("Formatted: script, script") #debug
        return script

    def generateDisplayBox(self):

        self.scriptDisplay = DirectFrame(
                        frameColor=(0, 0, 0, 0),
                        frameSize=(-1.5, 1.5, -0.85, 0.85),
                        pos=(0, 0, 0))
        
        titleText = 'Script'

        self.backImage = OnscreenImage(
            self.pauseMenu.manager.black,
            parent=self.scriptDisplay,
            scale=(1.75, 0.9, 0.9),
            pos=(0, 0, 0)
        )

        self.backImage.setColor(0, 0, 0, 0.8)
        self.backImage.setTransparency(TransparencyAttrib.MAlpha)
        
        title= DirectLabel(
                        parent=self.scriptDisplay,
                        text= titleText,
                        text_scale= (0.110, 0.110),
                        pos= (0, 0, 0.767),
                        frameColor= (0, 0, 0, 0),
                        text_fg = (255, 255, 255, 1),
                        text_font = self.pauseMenu.manager.font)

        dialogue_texts = self.getScript()
      #  print("Dialogue texts for display:", dialogue_texts) # debug
        print("Creating GUI elements for ScriptDisplay") # debug

        line_height= 0.1
        margin= 0.25
        num_lines= len(dialogue_texts)

        #Finding width of longest line
        textNode= TextNode("temp")
        textScale= 0.05
        maxTextWidth=0

        for line in dialogue_texts:
            textNode.setText(line)
            line_width= textNode.getWidth() * textScale
            maxTextWidth= max(maxTextWidth, line_width)

        #Calcuating canvas dimensions
        canvasWidth= maxTextWidth + 0.2
        canvasHeight= max(0.70, num_lines * line_height)
        canvasHeight += margin

        self.scriptBackground = OnscreenImage(
            "../Assets/Images/paper.jpg",
            pos = (0, 0, 0),
            scale = (1.5,0,0.7),
            parent = self.scriptDisplay,
            
        )


        scrollableFrame = DirectScrolledFrame(
                                            parent= self.scriptDisplay,
                                            frameSize= (-1.5, 1.5, -0.70, 0.70),
                                            frameColor= (0, 0, 0, 0),
                                            pos= (0, 0, 0),
                                            scrollBarWidth= 0.05,
                                            canvasSize=(-canvasWidth/2, canvasWidth/2, -canvasHeight, margin)    ,
                                            horizontalScroll_decButton_relief=None,
                                            horizontalScroll_incButton_relief=None,
                                            horizontalScroll_frameSize=(0, 0, 0, 0),
                                        )
        

        for i, text in enumerate(dialogue_texts):
            textYPos= margin - (i * line_height) - 0.1
            DirectLabel(
                parent= scrollableFrame.getCanvas(),
                text= text,
                text_align= TextNode.ALeft,
                text_scale= textScale,
                pos=(-canvasWidth/2 + line_height, 0, textYPos),
                frameColor=(0, 0, 0, 0),
                text_fg=(0, 0, 0, 1),
                text_wordwrap= 55
            )
        count = text.count('\n') + 1
        p = textYPos
        p -= margin * count
        bottom = p - 0.2  
        scrollableFrame['canvasSize'] = (-canvasWidth/2, canvasWidth/2, bottom, margin)
        self.scriptBackground.setBin("fixed", 0)

        self.exitScriptButton = DirectButton(
            text="Back",
            text_font = self.pauseMenu.manager.font,
            scale=0.1,
            pos=(0, 0, -0.85),
            parent=self.scriptDisplay,
            command=self.goBackToPauseMenu,
            frameColor = (0, 0, 0, 0.0),
            text_fg = (1, 1, 1, 1)
        )

        self.scriptBackground.setBin("fixed", 20)
        self.backImage.setBin("fixed", 10)

        self.setButtonHover()

        # self.getConversation() 


    def show(self):
        print("Displaying ScriptDisplay") # debug
        self.scriptDisplay.show()
        
    def goBackToPauseMenu(self):
        self.hide()
        self.pauseMenu.show()

    def hide(self):
        self.scriptDisplay.hide()
        
    def returnToPause(self):
        self.hide()
        self.manager.show()

    def setButtonHover(self):
        self.exitScriptButton.bind(DGG.ENTER, lambda event: self.pauseMenu.manager.setColorHover(self.exitScriptButton)) 
        self.exitScriptButton.bind(DGG.EXIT, lambda event: self.pauseMenu.manager.setColorDefault(self.exitScriptButton)) 

    def updateFont(self):
        self.exitScriptButton["text_font"] = self.pauseMenu.manager.font
        self.exitScriptButton["text_font"] = self.pauseMenu.manager.font
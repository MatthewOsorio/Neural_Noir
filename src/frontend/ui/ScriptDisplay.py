from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectLabel import DirectLabel
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectScrolledFrame import DirectScrolledFrame
from direct.gui.DirectButton import DirectButton
from panda3d.core import TextNode

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
            script.append(f"Detective: {interaction[0]}")
            script.append(f"Player: {interaction[1]}")

        return script
    
    def getScript(self):
        print("Getting script")
        sessionID = self.gameManager._sessionController.getSessionID()
        conversation = self.gameManager._database.fetchConversation(sessionID)

        print("Fetched conversation from DB: ", conversation) # debug
        script = self.formatScript(conversation)
        print("Formatted: script, script") #debug
        return script

    def generateDisplayBox(self):

        self.scriptDisplay = DirectFrame(
                        frameColor=(0, 0, 0, 0),
                        frameSize=(-1.5, 1.5, -0.85, 0.85),
                        pos=(0, 0, 0))
        
        titleText = 'Script'
    
        title= DirectLabel(
                        parent=self.scriptDisplay,
                        text= titleText,
                        text_scale= (0.110, 0.110),
                        pos= (-1.355, 0, 0.767),
                        frameColor= (0, 0, 0, 0),
                        text_fg = (255, 255, 255, 1))

        dialogue_texts = self.getScript()
        print("Dialogue texts for display:", dialogue_texts) # debug
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

        scrollableFrame = DirectScrolledFrame(
                                            parent= self.scriptDisplay,
                                            frameSize= (-1.5, 1.5, -0.70, 0.70),
                                            frameColor= (0, 0, 0, 0.7),
                                            pos= (0, 0, 0),
                                            scrollBarWidth= 0.05,
                                            canvasSize=(-canvasWidth/2, canvasWidth/2, -canvasHeight, margin)    
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
                text_fg=(1, 1, 1, 1)
            )

        self.exitScriptButton = DirectButton(
            text="Back",
            scale=0.1,
            pos=(-1.385, 0, -0.85),
            parent=self.scriptDisplay,
            command=self.goBackToPauseMenu
        )

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
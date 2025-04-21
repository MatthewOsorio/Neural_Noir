from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectFrame, DirectButton, DGG
from panda3d.core import TextNode
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
import sys
from panda3d.core import TransparencyAttrib

#ConfirmQuit code originally written by Matt
#Modified and integrated by Evie 
class confirmQuit:

    def __init__(self, manager, base):
        self.manager = manager
        self.base = base

        self.createContents()
        self.createContentFromPause()
        self.hide()

    def createContents(self):
        self.parentFrame = DirectFrame(
            frameColor=(0, 0, 0, 0),
            frameSize=(-0.75, 0.75, -0.75, 0.75),
            pos= (0, 0, 0),
            parent=self.base.aspect2d)
        
        self.backdrop = OnscreenImage(
            self.manager.mainBackground,
            pos = (1, 0, 0), 
            parent = self.parentFrame)
        
        self.backdropBack = OnscreenImage(
            self.manager.black,
            pos = (-1, 0, 0),
            parent = self.parentFrame
        )
        
        titleText= 'Are you sure you want to quit?'
        #TitleFrame= DirectFrame(parent= parentFrame,
                                #frameColor= (0, 0, 0, 0),
                                #frameSize= (-0.50, 0.50, -0.25, 0.25),
                                #pos= (0, 0, 0.5))
        
        self.titleTextFrame= DirectLabel(parent= self.parentFrame,
            text= titleText,
            text_scale= (0.1, 0.1),
            text_fg= (255, 255, 255, 0.9),
            frameColor= (0, 0, 0, 0),
            pos = (-1,0.5,0.5))
        
        self.yesButton= DirectButton(parent= self.parentFrame,
            text="Yes",
            scale= 0.1,
            pos= (-1.3, 0, 0),
            command = sys.exit,
            frameColor = (0, 0, 0, 0.0),
            text_fg = (1, 1, 1, 1),
            text_font = self.manager.font)
        
        self.noButton= DirectButton(parent= self.parentFrame,
            text="No",
            scale= 0.1,
            pos= (-0.7, 0, 0),
            command = self.moveToMain,
            frameColor = (0, 0, 0, 0.0),
            text_fg = (1, 1, 1, 1), 
            text_font = self.manager.font)

        self.yesButton.bind(DGG.ENTER, lambda event: self.manager.setColorHover(self.yesButton)) 
        self.yesButton.bind(DGG.EXIT, lambda event: self.manager.setColorDefault(self.yesButton)) 
    
        self.noButton.bind(DGG.ENTER, lambda event: self.manager.setColorHover(self.noButton)) 
        self.noButton.bind(DGG.EXIT, lambda event: self.manager.setColorDefault(self.noButton))  

    def createContentFromPause(self):
        self.parentFramePause = DirectFrame(
            frameColor=(0, 0, 0, 0),
            frameSize=(-0.75, 0.75, -0.75, 0.75),
            pos= (0, 0, 0),
            parent=self.base.aspect2d)
        
        self.backImage = OnscreenImage(
            self.manager.black,
            parent=self.parentFramePause,
            scale=(1.5, 0.9, 0.9),
            pos=(0, 0, 0)
        )

        self.backImage.setColor(0, 0, 0, 0.8)
        self.backImage.setTransparency(TransparencyAttrib.MAlpha)
        
        self.titleTextFrame= DirectLabel(
            parent= self.parentFramePause,
            text= "Quit to the main menu?",
            text_font = self.manager.font,
            text_scale= (0.15, 0.15),
            text_fg= (255, 255, 255, 0.9),
            frameColor= (0, 0, 0, 0),
            pos = (0,0.5,0.5))
    
        self.warningText = OnscreenText(
            text = "Warning: Progress will not be saved!",
            #font = self.manager.font,
            scale = 0.075,
            parent = self.parentFramePause,
            fg = (1, 0, 0, 1),
            pos = (0,0.3,0.3)
        )
        
        self.yesButtom= DirectButton(
            parent= self.parentFramePause,
            text_font = self.manager.font,
            text="Yes",
            scale= 0.075,
            pos= (-0.40, 0, 0),
            command = self.pauseReturn,
            frameColor = (0, 0, 0, 0.0),
            text_fg = (1, 1, 1, 1)
            )
        
        self.noButtom= DirectButton(
            parent= self.parentFramePause,
            text_font = self.manager.font,
            text="No",
            scale= 0.075,
            pos= (0.40, 0, 0),
            command = self.manager.showPauseHideQuit,
            frameColor = (0, 0, 0, 0.0),
            text_fg = (1, 1, 1, 1)
            )
        
        self.yesButtom.bind(DGG.ENTER, lambda event: self.manager.setColorHover(self.yesButtom)) 
        self.yesButtom.bind(DGG.EXIT, lambda event: self.manager.setColorDefault(self.yesButtom)) 
    
        self.noButtom.bind(DGG.ENTER, lambda event: self.manager.setColorHover(self.noButtom)) 
        self.noButtom.bind(DGG.EXIT, lambda event: self.manager.setColorDefault(self.noButtom))     

    def moveToMain(self):
        self.hide()
        self.manager.showMain()
    
    def show(self):
        self.parentFrame.show()
        self.parentFramePause.show()
    
    def hide(self):
        self.parentFrame.hide()
        self.parentFramePause.hide()

    def hideParent(self):
        self.parentFrame.hide()

    def showParent(self):
        self.parentFrame.show()
    
    def showFromPause(self):
        self.parentFramePause.show()
    
    def hideFromPause(self):
        self.parentFramePause.hide()
    
    def pauseReturn(self):
        self.hideFromPause()
        if self.manager.pauseMenu != None:
            self.manager.pauseMenu.returnToMain()

    def updateFont(self):
        self.yesButtom["text_font"] = self.manager.font
        self.noButtom["text_font"] = self.manager.font
        self.yesButton["text_font"] = self.manager.font
        self.noButton["text_font"] = self.manager.font
        self.titleTextFrame["text_font"] = self.manager.font    

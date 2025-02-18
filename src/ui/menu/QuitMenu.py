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
            scale= 0.1,
            pos= (-0.40, 0, 0),
            command = sys.exit)
        
        self.noButtom= DirectButton(parent= self.parentFrame,
            text="No",
            scale= 0.1,
            pos= (0.40, 0, 0),
            command = self.moveToMain)
        
    def createContentFromPause(self):
        self.parentFramePause = DirectFrame(
            frameColor=(0, 0, 0, 0),
            frameSize=(-0.75, 0.75, -0.75, 0.75),
            pos= (0, 0, 0),
            parent=self.base.aspect2d)
        
        self.backImage = OnscreenImage(
            self.manager.backGroundBlack,
            parent=self.parentFramePause,
            scale=(1.5, 0.9, 0.9),
            pos=(0, 0, 0)
        )

        self.backImage.setColor(0, 0, 0, 0.5)
        self.backImage.setTransparency(TransparencyAttrib.MAlpha)
        
        self.titleTextFrame= DirectLabel(
            parent= self.parentFramePause,
            text= "Quit to the main menu?",
            text_font = loader.loadFont(self.manager.limeLight),
            text_scale= (0.15, 0.15),
            text_fg= (255, 255, 255, 0.9),
            frameColor= (0, 0, 0, 0),
            pos = (0,0.5,0.5))
    
        self.warningText = OnscreenText(
            text = "Warning: Progress will not be saved",
            font = loader.loadFont(self.manager.limeLight),
            scale = 0.075,
            parent = self.parentFramePause,
            fg = (1, 0, 0, 1),
            pos = (0,0.3,0.3)
        )
        
        self.yesButtom= DirectButton(
            parent= self.parentFramePause,
            text_font = loader.loadFont(self.manager.limeLight),
            text="Yes",
            scale= 0.075,
            pos= (-0.40, 0, 0),
            command = self.pauseReturn
            )
        
        self.noButtom= DirectButton(
            parent= self.parentFramePause,
            text_font = loader.loadFont(self.manager.limeLight),
            text="No",
            scale= 0.075,
            pos= (0.40, 0, 0),
            command = self.manager.showPauseHideQuit
            )
        
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
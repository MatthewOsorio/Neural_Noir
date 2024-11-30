from direct.showbase.ShowBase import ShowBase
from direct.showbase.Transitions import Transitions
from panda3d.core import TextNode
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from direct.interval.IntervalGlobal import *
# import sys     implement for sys.exit() later on

class ConnectionDisplay(ShowBase):
    def __init__(self, base) :
        self.base = base
        
        self.text = TextNode('connectionDisplayText')
        self.text.setAlign(TextNode.ACenter)
        self.textNodePath = self.base.aspect2d.attachNewNode(self.text)
        self.textNodePath.setScale(0.1)
        self.textNodePath.setPos(0, 0, 0)

        self.background = OnscreenImage(
            image = '../images/black_background_832x472.png',
            parent = self.base.render2d
        )

    def displayCheckingInternet(self):
        self.text.setText("Checking internet connection...")

    def displayEstablishingConn(self):
        self.text.setText("Establishing connection with OpenAI...")

    def displayInternetOffline(self):
        self.text.setText('''Internet is offline\n\n Please check your connection and restart the game''')
        
    def displayUnableToEstablishConn(self):
        self.text.setText("Unable to establish a connection\n\n Please report this to the development team:\n placeholder@gmail.com")
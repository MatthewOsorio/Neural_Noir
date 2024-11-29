from direct.showbase.ShowBase import ShowBase
from direct.showbase.Transitions import Transitions
from panda3d.core import TextNode
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from direct.interval.IntervalGlobal import *
# import sys    # implement for sys.exit() later on

class ConnectionDisplay:
    def __init__(self, base):
        self.base = base

        

        self.titleImage = OnscreenImage(
            image = '../images/black_background_832x472.png',
            parent = self.base.render2d
        )

    def displayCheckingInternet(self):
        self.textObject = OnscreenText(
            text='Checking internet connection...',
            scale=0.1,
            pos=(0,0)
        )

    def displayEstablishingConn(self):
        self.textObject = OnscreenText(
            text='Establishing connection with OpenAI...',
            scale=0.1,
            pos=(0,0)
        )

    def displayInternetOffline(self):
        self.textObject = OnscreenText(
            text='Internet is offline. Please check your connection and restart the game',
            scale=0.1,
            pos=(0,0)
        )

    def displayUnableToEstablishConn(self):
        self.textObject = OnscreenText(
            text='''Unable to establish a connection

                    Please report this to the development team:
                    placeholder@gmail.com
                    ''',
            scale=0.1,
            pos=(0,0)
        )
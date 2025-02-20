from direct.showbase.ShowBase import ShowBase
from direct.showbase.Transitions import Transitions # add transitions between connection test screens
from panda3d.core import TextNode
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from direct.interval.IntervalGlobal import *

class ConnectionDisplay:
    def __init__(self, base, connection):
        self.base = base
        self.connection = connection # dependency injection of connection_util
        
        self.text = TextNode('connectionDisplayText')
        self.text.setAlign(TextNode.ACenter)
        self.textNodePath = self.base.aspect2d.attachNewNode(self.text)
        self.textNodePath.setScale(0.1)
        self.textNodePath.setPos(0, 0, 0)

    def initializeBackground(self):

        self.background = OnscreenImage(
            image='../images/black_background_832x472.png',
            parent=self.base.render2d,
            sort=0
        )
        self.background.show()
        self.background.setName("ConnectionDisplayBackground") # for debugging nodes

    def displayCheckingInternet(self):
        self.initializeBackground()
        self.text.setText("Checking internet connection...")

    def displayEstablishingConn(self):
        self.initializeBackground()
        self.text.setText("Establishing connection with OpenAI...")

    def displayInternetOffline(self):
        self.initializeBackground()
        self.text.setText('''Internet is offline\n\n Please check your connection and restart the game''')
        
    def displayUnableToEstablishConn(self):
        self.initializeBackground()
        self.text.setText("Unable to establish a connection\n\n Please report this to the development team:\n placeholder@gmail.com")

    def checkInternetAndDisplay(self, on_success, on_failure):
        self.displayCheckingInternet()

        # delay for 2 seconds
        self.base.taskMgr.doMethodLater(2, self._checkInternet, "Check Internet",
                                        extraArgs=[on_success, on_failure])

    def _checkInternet(self, on_success, on_failure):
        if not self.connection.checkInternet(): # if internet is not connected, exit program (instruction in main)
            self.displayInternetOffline()
            self.base.taskMgr.doMethodLater(3, on_failure, "Internet Offline Exit")
            return

        self.displayEstablishingConn() # if successful, send a test message to OpenAI
        self.base.taskMgr.doMethodLater(2, self._checkOpenai, "Check OpenAI",
                                        extraArgs=[on_success, on_failure])

    def _checkOpenai(self, on_success, on_failure): # exit program (instruction in main) if test message cannot be sent
        if not self.connection.checkOpenai():
            self.displayUnableToEstablishConn()
            self.base.taskMgr.doMethodLater(3, on_failure, "OpenAI Failure Exit")
            return

        self.destroyConnectionStatus()
        on_success()  # load interrogation room, NLP, SR, and TTS systems

    def destroyConnectionStatus(self):
        # destroy the connection status nodes before loading in the interrogation room to prevent overlapping of scenes
        if self.textNodePath:
            self.textNodePath.removeNode()  # remove the text node
            self.textNodePath = None
        if self.background:
            self.background.destroy()  # destroy the background
            self.background = None

        # hide scenes before loading in interrogation room
        for child in self.base.render2d.getChildren():
            if child.getName() == "ConnectionDisplayBackground":
                child.hide()
        for child in self.base.render2d.getChildren():
            if child.getName() == "MainMenuBackground":
                child.hide()
        for child in self.base.render2d.getChildren():
            if child.getName() == "OnscreenImage":
                child.hide()

        # for debugging nodes
        print("Remaining children in render2d:")
        for child in self.base.render2d.getChildren():
            print(f"Child: {child}")
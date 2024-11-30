from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectFrame, DirectButton, DGG
from panda3d.core import TextNode
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import *
from direct.gui.OnscreenText import OnscreenText
import time 

from ui.connectionDisplay import ConnectionDisplay

# Main Application for Testing
class MyApp(ShowBase):
    def __init__(self):
        super().__init__()

        # Initialize ConnectionDisplay
        self.connDisplay = ConnectionDisplay(self)

        # Test display functions
        self.testDisplayCheckingInternet()

    def testDisplayCheckingInternet(self):
        self.connDisplay.displayCheckingInternet()

    def testDisplayEstablishingConn(self):
        self.connDisplay.displayEstablishingConn()

    def testDisplayInternetOffline(self):
        self.connDisplay.displayInternetOffline()

    def testDisplayUnableToEstablishConn(self):
        self.connDisplay.displayUnableToEstablishConn()


# Run the Application
app = MyApp()
app.run()
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectFrame, DirectButton, DGG
from panda3d.core import TextNode
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import *
from direct.gui.OnscreenText import OnscreenText
import time 

import menu
import InterrogationRoom


class main(ShowBase):
    def __init__(self):
        super().__init__()

        self.menuManager = menu.menuManager(self)
        self.interrogationRoom = InterrogationRoom.InterrogationRoom(self)

        self.menuManager.showMain()


app = main()
app.run()
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectFrame, DirectButton, DGG
from panda3d.core import TextNode
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *


import os
from panda3d.core import Filename
current_dir = os.path.dirname(os.path.abspath(__file__))

class Evidence:
    def __init__(self, base):
        self.base = base

        self.active = False
        early1 = os.path.join(current_dir, "..", "..", "..", "..", "Assets", "Images", "Evidence", "early1.png")
        early1 = os.path.normpath(early1)
        early1 = Filename.fromOsSpecific(early1).getFullpath()

        early2 = os.path.join(current_dir, "..", "..", "..", "..", "Assets", "Images", "Evidence", "early2.png")
        early2 = os.path.normpath(early2)
        early2 = Filename.fromOsSpecific(early2).getFullpath()

        early3 = os.path.join(current_dir, "..", "..", "..", "..", "Assets", "Images", "Evidence", "early3.png")
        early3 = os.path.normpath(early3)
        early3 = Filename.fromOsSpecific(early3).getFullpath()

        mid1 = os.path.join(current_dir, "..", "..", "..", "..", "Assets", "Images", "Evidence", "mid1.png")
        mid1 = os.path.normpath(mid1)
        mid1 = Filename.fromOsSpecific(mid1).getFullpath()

        mid2 = os.path.join(current_dir, "..", "..", "..", "..", "Assets", "Images", "Evidence", "mid2.png")
        mid2 = os.path.normpath(mid2)
        mid2 = Filename.fromOsSpecific(mid2).getFullpath()

        mid3 = os.path.join(current_dir, "..", "..", "..", "..", "Assets", "Images", "Evidence", "mid3.png")
        mid3 = os.path.normpath(mid3)
        mid3 = Filename.fromOsSpecific(mid3).getFullpath()       

        final1 = os.path.join(current_dir, "..", "..", "..", "..", "Assets", "Images", "Evidence", "final1.png")
        final1 = os.path.normpath(final1)
        final1 = Filename.fromOsSpecific(final1).getFullpath()     

        final2 = os.path.join(current_dir, "..", "..", "..", "..", "Assets", "Images", "Evidence", "final2.png")
        final2 = os.path.normpath(final2)
        final2 = Filename.fromOsSpecific(final2).getFullpath()     

        final3 = os.path.join(current_dir, "..", "..", "..", "..", "Assets", "Images", "Evidence", "final3.png")
        final3 = os.path.normpath(final3)
        final3 = Filename.fromOsSpecific(final3).getFullpath()     

        final4 = os.path.join(current_dir, "..", "..", "..", "..", "Assets", "Images", "Evidence", "final4.png")
        final4 = os.path.normpath(final4)
        final4 = Filename.fromOsSpecific(final4).getFullpath()  

        self.imageDict = {
            "early1.png" : early1,
            "early2.png" : early2,
            "early3.png" : early3,
            "mid1.png" : mid1,
            "mid2.png" : mid2,
            "mid3.png" : mid3,
            "final1.png" : final1,
            "final2.png" : final2,
            "final3.png" : final3,
            "final4.png" : final4
        }

        self.evidence = DirectFrame(
            frameColor=(0, 0, 0, 0),
            frameSize=(-1, 1, -1, 1),
            parent=self.base.base.aspect2d
        )

        self.evidenceImage = OnscreenImage(
            self.base.base.menuManager.room,
            parent=self.evidence,
            scale=(1.5, 0.8, 0.8),
            pos=(0 , 0, 0),
        )    

        self.button = DirectButton(
            text = "Next",
            command = None,
            sortOrder = 1,
            text_font = self.base.menu.font,
            text_fg = (1, 1, 1, 1),
            frameColor = (0, 0, 0, 0.8),
            pos = (-1.7, -0.9, -0.9),
            scale = 0.1,
            parent = self.evidence
        )

        self.hide()

    def setImage(self, image):
        self.evidenceImage.setImage(self.imageDict[image])

    def show(self):
        self.evidence.show()

    def hide(self):
        self.evidence.hide()
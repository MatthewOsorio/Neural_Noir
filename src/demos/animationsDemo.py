from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import Filename
import os

class TestAnimations(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()

        self.dir = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "blender", "converted_animations"))
        self.animations = os.path.join(dir, "..", "..", "blender", "converted_animations")
        self.animations = os.path.normpath(self.animations)

        self.harris = Actor(
            self.pandaPath("harris.bam"),
            {
                "bang": self.pandaPath("")
                "lean": self.pandaPath
                "stand": self.pandaPath
                "idle": self.pandaPath
                "laugh": self.pandaPath
                "sit": self.pandaPath
            }
        )

    def pandaPath(self, filename):
        return Filename.fromOsSpecific(os.path.join(self.animations, filename)).getFullpath()






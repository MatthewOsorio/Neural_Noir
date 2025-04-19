from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import Filename
import os

class TestAnimations(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()
        self.camera.setPos(0, 0, 2)      
        self.camera.lookAt(0, 5, -1.5)


        self.animations = os.path.normpath(os.path.join(
            os.path.dirname(__file__), "..", "..", "blender", "converted_animations"
            ))

        # Harris test
        self.harris = Actor(
            self.pandaPath("harris.bam"),
            {
                "bang": self.pandaPath("harris_banging_fist.bam"),
                "lean": self.pandaPath("harris_male_sitting_back_pose.bam"),
                "stand": self.pandaPath("harris_sitting_idle.bam"),
                "idle": self.pandaPath("harris_sitting_idle.bam"),
                "laugh": self.pandaPath("harris_sitting_laughing.bam"),
                "sit": self.pandaPath("harris_stand_to_sit.bam")
            }
        )
        self.harris.reparentTo(self.render)
        self.harris.setScale(0.5)
        self.harris.setPos(-1, 5, -1.5)
        self.harris.loop("idle")

        self.accept("1", self.playAnim, [self.harris, "idle"])
        self.accept("2", self.playAnim, [self.harris, "laugh"])
        self.accept("3", self.playAnim, [self.harris, "bang"])
        self.accept("4", self.playAnim, [self.harris, "lean"])
        self.accept("5", self.playAnim, [self.harris, "stand"])
        self.accept("6", self.playAnim, [self.harris, "sit"])

        # Miller test
        self.miller = Actor(
            self.pandaPath("miller.bam"),
            {
                "lean": self.pandaPath("miller_male_sitting_back_pose.bam"),
                "stand": self.pandaPath("miller_sit_to_stand.bam"),
                "idle": self.pandaPath("miller_sitting_idle.bam"),
                "sit": self.pandaPath("miller_stand_to_sit.bam"),
                "talk": self.pandaPath("miller_talking.bam")
            }
        )
        self.miller.reparentTo(self.render)
        self.miller.setScale(0.5)
        self.miller.setPos(1, 5, -1.5)
        self.miller.loop("idle")

        self.accept("7", self.playAnim, [self.miller, "lean"])
        self.accept("8", self.playAnim, [self.miller, "stand"])
        self.accept("9", self.playAnim, [self.miller, "idle"])
        self.accept("0", self.playAnim, [self.miller, "sit"])
        self.accept("-", self.playAnim, [self.miller, "talk"])

    def playAnim(self, actor, anim_name):
        actor.stop()
        actor.play(anim_name)    

    def pandaPath(self, filename):
        return Filename.fromOsSpecific(os.path.join(self.animations, filename)).getFullpath()

if __name__ == "__main__":
    TestAnimations().run()


from direct.actor.Actor import Actor

class Animations:
    def __init__(self, base):
        self.base = base

        # Load in Harris
        self.harris = Actor(
            "../blender/converted_animations/harris.bam",
            {

                "idle": "../blender/converted_animations/harris_sitting_idle.bam",
                "laugh": "../blender/converted_animations/harris_sitting_laughing.bam",
                "bang": "../blender/converted_animations/harris_banging_fist.bam",
                "lean": "../blender/converted_animations/harris_male_sitting_back_pose.bam",
                "stand": "../blender/converted_animations/harris_sit_to_stand.bam",
                "sit": "../blender/converted_animations/harris_stand_to_sit.bam"
            }
        )
        self.harris.setScale(1)
        # Visibility for Harris
        self.harris.setLightOff()
        self.harris.setColor((1, 1, 1, 1))
        self.harris.show()
        self.harris.setBin("opaque", 10)
        self.harris.setDepthTest(True)
        self.harris.setDepthWrite(True)

        # Load in Miller
        self.miller = Actor(
            "../blender/converted_animations/miller.bam",
            {
                "idle": "../blender/converted_animations/miller_sitting_idle.bam",
                "talk": "../blender/converted_animations/miller_talking.bam",
                "lean": "../blender/converted_animations/miller_male_sitting_back_pose.bam",
                "sit": "../blender/converted_animations/miller_stand_to_sit.bam",
                "stand": "../blender/converted_animations/miller_sit_to_stand.bam"
            }
        )
        self.miller.setScale(1)
        # Visibility for miller
        self.miller.setLightOff()
        self.miller.setBin("fixed", 150)
        self.miller.setDepthTest(True)
        self.miller.setDepthWrite(True)
        self.miller.setTransparency(False)
        self.miller.setTwoSided(True)

    def playHarrisIdle(self):
        self.harris.loop("idle")
        self.harris.setPos(0.6, 2.5, -1.1)
        self.harris.setH(-15)
        self.harris.reparentTo(self.base.render)

    def playHarrisLaugh(self):
        self.harris.loop("laugh")
        self.harris.setPos(0.6, 2.4, -1.1) #(leftright, forwardbackward, updown)
        self.harris.setH(-15)
        self.harris.reparentTo(self.base.render)

    def playHarrisBang(self):
        self.harris.loop("bang")
        self.harris.setPos(0.5, 2.2, -1.16) #(-leftright+, -forwardbackward+, updown)
        self.harris.setH(-15)
        self.harris.reparentTo(self.base.render)

    def playHarrisLean(self):
        self.harris.loop("lean")
        self.harris.setPos(0.6, 2.2, -1.17) #(leftright, forwardbackward, updown)
        self.harris.setH(-23)
        self.harris.reparentTo(self.base.render)

    def playHarrisStand(self):
        self.harris.loop("stand")
        self.harris.setPos(0.6, 2.55, -1.1) #(leftright, forwardbackward, updown)
        self.harris.setH(-15)
        self.harris.reparentTo(self.base.render)

    def playHarrisSit(self):
        self.harris.loop("sit")
        self.harris.setPos(0.5, 2, -1.1) #(leftright, forwardbackward, updown)
        self.harris.setH(-15)
        self.harris.reparentTo(self.base.render)

    def playMillerIdle(self):
        self.miller.loop("idle")
        self.miller.setPos(-0.35, 2.3, -1.1) #(leftright, forwardbackward, updown)
        self.miller.setH(4)
        self.miller.reparentTo(self.base.render)

    def playMillerTalk(self):
        self.miller.loop("talk")
        self.miller.setPos(-0.35, 2.2, -1.14) #(leftright, forwardbackward, updown)
        self.miller.setH(4)
        self.miller.reparentTo(self.base.render)

    def playMillerLean(self):
        self.miller.loop("lean")
        self.miller.setScale(1)
        self.miller.setPos(-0.35, 2.2, -1.1) #(leftright, forwardbackward, updown)
        self.miller.setH(4)
        self.miller.reparentTo(self.base.render)

    def playMillerSit(self):
        self.miller.loop("sit")
        self.miller.setPos(-0.35, 1.9, -1.1) #(leftright, forwardbackward, updown)
        self.miller.setH(4)
        self.miller.reparentTo(self.base.render)

    def playMillerStand(self):
        self.miller.loop("stand")
        self.miller.setPos(-0.35, 2.3, -1.1) #(leftright, forwardbackward, updown)
        self.miller.setH(4)
        self.miller.reparentTo(self.base.render)

    def resetHarris(self):
        self.playHarrisIdle()

    def resetMiller(self):
        self.playMillerIdle()
    
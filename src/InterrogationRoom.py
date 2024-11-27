from direct.showbase.ShowBase import ShowBase

#Code originally written by Christine 
#Modified by Evie 
class InterrogationRoom:
    def __init__(self, base):
        self.base = base

        # Disable deafult mouse controls
        self.base.disableMouse()

        self.cameraSetUp = cameraSetUp(self.base)

        # Load the room model
        self.room = self.base.loader.loadModel("../blender/converted_room_whole/room.bam")
        self.room.reparentTo(self.base.render)
        self.room.setScale(1)
        self.room.setPos(5.6, 6, 0.2)
        self.room.setHpr(0, 0, 0)


class cameraSetUp:
    def __init__(self, base):
        self.base = base

        #Moved the camera back slightly so that it does not clip the table
        self.base.camera.setPos(0, -0.2 , 0)
        #Test print for the camera position if we need to change it
        #print(self.base.camera.getPos())

        self.cameraSensitivity = 10
        self.horizontal = 0
        self.vertical = 0

        #Updates the camera angle
        self.base.taskMgr.add(self.moveCamera, "Move Camera")

    #Allows users to rotate the camera slightly to "look around"
    def moveCamera(self, base):
        if self.base.mouseWatcherNode.hasMouse():
            self.x = self.base.mouseWatcherNode.getMouseX()
            self.y = self.base.mouseWatcherNode.getMouseY()

            #X value multiplied by -1 so that the horizontal camera movement is not inverted
            self.horizontal = (self.x * self.cameraSensitivity) * -1
            self.vertical = self.y * self.cameraSensitivity

            self.base.camera.setHpr(self.horizontal, self.vertical, 0)

            #Test for x and y coordinates 
            #print("X: ", self.x, " ", "Y: ", self.y)

        return base.cont


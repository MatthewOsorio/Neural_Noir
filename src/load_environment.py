from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase, Camera
from direct.task import Task
from panda3d.core import Point3
import direct.directbase.DirectStart 
from pandac.PandaModules import *


class InterrogationRoom(ShowBase):
    def __init__(self):
        # Initialize the ShowBase class
        ShowBase.__init__(self)

        # Disable default mouse-based camera controls
        # self.disable_mouse()

        # Load the environment model
        self.scene = self.loader.loadModel("models/neural_noir/converted_room_whole/room.bam")
        self.scene.reparentTo(self.render)
        self.scene.setScale(1)
        self.scene.setPos(0, 0, 0)
        self.scene.set_scene

        # Position the camera inside the room
        # self.camera.setPos(200, 0, 5)  # Inside the room, facing forward
        # self.camera.lookAt(0, 0, 5)    # Point the camera at the center

        # Add the camera spinning task to the task manager
        # self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

    # Define a procedure to move the camera
    # def spinCameraTask(self, task):
    #     angleDegrees = task.time * 6.0  # Rotate 6 degrees per second
    #     angleRadians = angleDegrees * (pi / 180.0)
    #     self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3)
    #     self.camera.setHpr(angleDegrees, 0, 0)
    #     return Task.cont


# Create an instance of the application
room = InterrogationRoom()

# Start the Panda3D main loop
room.run()

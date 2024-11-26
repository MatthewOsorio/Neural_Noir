from direct.showbase.ShowBase import ShowBase

class InterrogationRoom:
    def __init__(self, base):
        self.base = base

        # Disable deafult mouse controls
        self.base.disableMouse()

        # Load the room model
        self.room = self.base.loader.loadModel("../blender/converted_room_whole/room.bam")
        self.room.reparentTo(self.base.render)
        self.room.setScale(1)
        self.room.setPos(5.6, 6, 0.2)
        self.room.setHpr(0, 0, 0)



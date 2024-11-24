from direct.showbase.ShowBase import ShowBase

class InterrogationRoom(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Disable deafult mouse controls
        self.disableMouse()

        # Load the room model
        self.room = self.loader.loadModel("models/neural_noir/converted_room_whole/room.bam")
        self.room.reparentTo(self.render)
        self.room.setScale(1)
        self.room.setPos(5.6, 6, 0.2)
        self.room.setHpr(0, 0, 0)

room = InterrogationRoom()
room.run()

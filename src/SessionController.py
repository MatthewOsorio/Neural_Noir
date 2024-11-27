from datetime import datetime
from uuid import uuid4

class SessionController:
    def __init__(self, database):
        self.sessionID= uuid4()
        self.startTime= None
        self.endTime= None
        self.ending= None
        self.databaseAPI= database
    
    def start(self):
        self.startTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.databaseAPI.insertStartSession(self.sessionID, self.startTime)
        
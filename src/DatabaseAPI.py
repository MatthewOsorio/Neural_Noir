import psycopg

class DatabaseAPI:
    #Nothing is passed in and the connection to the database is established here, the cursor attribute is set as cursor object from psycopg
    def __init__(self):
        with psycopg.connect("Create connection here") as conn:
            with conn.cursor() as cur:
                self.__cursor= cur

    #Receive the times and biometric values query the database to insert the those values
    def insert(self, startTime, endTime, temperature, heartRate, skinConduction):
        pass
    
    #Recieve the times, discrepancy, and the user/nps interaction and insert into the database
    def insert(self, startTime, endTime, discrepancy, userInput, generatedResponse):
        pass
    
    #Recieve the biometric values we are looking for and query the database for them, returns a tuple
    def fetch(self, temperature, heartRate, skinConduction):
        pass
    
    #Recieve the userInput to query for the whole user/NPC interaction, returns a tuple
    def fetch(self, userInput):
        pass
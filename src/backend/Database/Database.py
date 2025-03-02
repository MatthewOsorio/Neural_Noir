import sqlite3
import os
import uuid

class Database:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), "neural_noir.db")
        self.initialize_db()

    def getConnection(self):
        try:
            conn = sqlite3.connect(self.db_path)
            return conn
        except sqlite3.Error as e:
            raise Exception("Error connecting to the database: ", e)
            
    def initialize_db(self):
        conn = self.getConnection()
        with conn:
            cur = conn.cursor()
            cur.executescript("""
               CREATE TABLE IF NOT EXISTS GameSession(
                    sessionID TEXT PRIMARY KEY,
                    sessionStartTime TEXT,
                    sessionEndTime TEXT
                );

                CREATE TABLE IF NOT EXISTS Interaction(
                    interactionID TEXT PRIMARY KEY,
                    startTime TEXT,
                    endTime TEXT,
                    userInput TEXT,
                    response TEXT,
                    sessionID TEXT,
                    feedbackID TEXT,
                    FOREIGN KEY (sessionID) REFERENCES GameSession(sessionID),
                    FOREIGN KEY (feedbackID) REFERENCES BiometricFeedback(feedbackID)
                );
                              
                CREATE TABLE IF NOT EXISTS BiometricFeedback(
                    feedbackID TEXT PRIMARY KEY,
                    startTime TEXT,
                    endTime TEXT,
                    stdDeviation REAL,
                    temperature REAL,
                    heartRate REAL,
                    skinConductance REAL,
                    sessionID TEXT,
                    interactionID TEXT,
                    FOREIGN KEY (sessionID) REFERENCES GameSession(sessionID),
                    FOREIGN KEY (interactionID) REFERENCES Interaction(interactionID)
                );
            """   
            )
        conn.close()
    
    def insertStartSession(self, sessionID, startTime):
        try:
            conn = self.getConnection()
            with conn:
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO GameSession(sessionID, sessionStartTime)
                    VALUES(?, ?)
                """, (str(sessionID), startTime))
        except sqlite3.Error as e:
            raise Exception("Error executing insert statement: ", e)

    def insertInteraction(self, start, end, userInput, response, sessionID, feedbackID):
        try:
            interactionID = str(uuid.uuid4())
            conn = self.getConnection()
            with conn:
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO Interaction (interactionID, startTime, endTime, userInput, response, sessionID, feedbackID)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (interactionID, start, end, userInput, response, sessionID, feedbackID))
        except sqlite3.Error as e:
            raise Exception("Error executing insert statement", e)
        
    def fetchConversation(self, sessionID):
        try:
            conn = self.getConnection()
            with conn:
                cur = conn.cursor()
                cur.execute("""
                    SELECT userInput, response
                    FROM Interaction
                    WHERE sessionID = ?
                """, (str(sessionID),))
                return cur.fetchall()
        except sqlite3.Error as e:
            raise Exception("Error retrieving conversation", e)
        
    def insertBiometrics(self, startTime, endTime, stdDeviation, temperature, heartRate, skinConductance, sessionID, interactionID):
        try:
            feedbackID = str(uuid.uuid4())
            conn = self.getConnection()
            with conn:
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO BiometricFeedback (feedbackID, startTime, endTime, stdDeviation, temperature, heartRate, skinConductance, sessionID, interactionID)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (feedbackID, startTime, endTime, stdDeviation, temperature, heartRate, skinConductance, sessionID, interactionID))
        except sqlite3.Error as e:
            raise Exception("Ereror inserting biometrics: ", e)

    def closeConnection(self):
        conn = self.getConnection()
        conn.close()
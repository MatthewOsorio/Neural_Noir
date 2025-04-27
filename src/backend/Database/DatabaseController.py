import sqlite3
import os
import uuid

#Note from Evie 
    # I added some more columns to the Interaction Table to account for both detectives responding
    # You may need to drop and recreate the table to get it to work. If so just uncomment the alterTable function and run the program once
    # Also, because one of our requirements is the ethical handling of data, I removed the biometric feedback table entirely 
    # Even though we weren't using it, for the sake of clarity 

class DatabaseController:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), "neural_noir.db")
        self.initializeDB()
        #self.alterTable()

    def getConnection(self):
        try:
            conn = sqlite3.connect(self.db_path)
            return conn
        except sqlite3.Error as e:
            raise Exception("Error connecting to the database: ", e)
            
    def initializeDB(self):
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
                    response TEXT,
                    Speaker TEXT,
                    sessionID TEXT,
                    feedbackID TEXT,
                    FOREIGN KEY (sessionID) REFERENCES GameSession(sessionID),
                    FOREIGN KEY (feedbackID) REFERENCES BiometricFeedback(feedbackID)
                );
                              
                CREATE TABLE IF NOT EXISTS Verdicts(
                    verdictID TEXT PRIMARY KEY,
                    evidence TEXT,
                    verdict TEXT,
                    sessionID TEXT,
                    FOREIGN KEY (sessionID) REFERENCES GameSession(sessionID)
                );                                          
            """   
            )
        conn.close()

  #  def alterTable(self):
     #   conn = self.getConnection()
     #   with conn:
          #  cur = conn.cursor()
          #  cur.execute("""
          #      DROP TABLE IF EXISTS Interaction
          #  """)
      #  conn.close()
        
    def insertStartSession(self, sessionID, startTime):
        try:
            conn = self.getConnection()
            with conn:
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO GameSession(sessionID, sessionStartTime)
                    VALUES(?, ?)
                """, (sessionID, startTime))
                conn.commit()
        except sqlite3.Error as e:
            raise Exception("Error executing insert statement: ", e)

    def insertInteraction(self, start, end, response, speaker, sessionID, feedbackID):
        try:
            interactionID = str(uuid.uuid4())
            conn = self.getConnection()
            with conn:
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO Interaction (interactionID, startTime, endTime, response, speaker, sessionID, feedbackID)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (interactionID, start, end, response, speaker, sessionID, feedbackID))
                conn.commit()
        except sqlite3.Error as e:
            raise Exception("Error executing insert statement", e)
        
    def insertVerdict(self, sessionID, evidence, verdict):
        try:
            conn = self.getConnection()
            verdictID = str(uuid.uuid4())
            with conn:
                cur = conn.cursor()
                cur.execute("""
                        INSERT INTO Verdicts(verdictID, evidence, verdict, sessionID)
                        VALUES (?, ?, ?, ?)
                            """, (verdictID, evidence, verdict, sessionID))
        except sqlite3.Error as e:
            raise Exception("Error executing insert statement", e)

    def fetchVerdict(self, sessionID):
        try: 
            conn = self.getConnection()
            with conn:
                cur = conn.cursor()
                cur.execute("""
                        SELECT evidence, verdict
                        FROM Verdicts
                        WHERE sessionID = ?
                    """, (str(sessionID),))

                return cur.fetchall()
        except sqlite3.Error as e:
            raise Exception("Error retrieving conversation", e)
        
    def fetchConversation(self, sessionID):
        try:
            conn = self.getConnection()
            with conn:
                cur = conn.cursor()
                cur.execute("""
                    SELECT speaker, response
                    FROM Interaction
                    WHERE sessionID = ?
                """, (str(sessionID),))
                return cur.fetchall()
        except sqlite3.Error as e:
            raise Exception("Error retrieving conversation", e)
        
    def closeConnection(self):
        conn = self.getConnection()
        conn.close()
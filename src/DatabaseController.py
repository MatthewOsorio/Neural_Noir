from psycopg import connect

class DatabaseController:
    def __init__(self):
        #Please change these to fit your environment
        self.dname= "NeuralNoir"
        self.user = "postgres"
        self.password = "password"
        self.host= "localhost"
        self.port = "5432"
    
    def getConnection(self):
        try:
            conn= connect(f"dbname= {self.dname} user= {self.user} password={self.password} host={self.host} port={self.port}")
            return conn
        except Exception as e:
            raise("Error connecting to the database: ", e)

    def insertStartSession(self, uuid, startTime):
        try:
            connection= self.getConnection()
            with connection.cursor() as cur:
                cur.execute("""
                                INSERT INTO GameSession(sessionID, sessionStartTime)
                                VALUES (%s, %s)
                            """, (uuid, startTime) 
                            )
                
            connection.commit() 

        except Exception as e:
            raise("Error executing insert statement", e)
        
    def insertInteraction(self, start, end, userInput, response, sessionID):
        try:
            connection= self.getConnection()
            with connection.cursor() as cur:
                cur.execute('''
                                INSERT INTO Interaction(interactionID, startTime, endTime, userInput, generatedResponse, sessionID)
                                VALUES(uuid_generate_v4(), %s, %s, %s, %s, %s)''', 
                                (start, end, userInput, response, sessionID)
                            )
                
            connection.commit()
        
        except Exception as e:
            raise("Error executing insert statment", e)
        
    def fetchConversation(self, sessionID):
        #Change onces its implemented
        temp = '3cc75489-4993-4e9a-a75a-1dfe9da8805f'
        try:
            connection = self.getConnection()
            with connection.cursor() as cur:
                cur.execute('''
                                SELECT generatedResponse, userInput 
                                FROM Interaction
                                WHERE sessionID= %s''',
                                (temp,)
                            )
                
                conversation = cur.fetchall()
                return conversation
        except Exception as e:
            raise("Error retrieving conversation", e)
        

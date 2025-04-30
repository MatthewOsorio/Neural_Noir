# import pytest
# import os
# import uuid
# import sqlite3
# from .context import DatabaseController

# TEST_DB_PATH = os.path.join(os.path.dirname(__file__), "test_neural_noir.db")

# @pytest.fixture
# def db():
#     database = DatabaseController()
#     database.db_path = TEST_DB_PATH
#     database.initializeDB()

#     yield database

#     database.closeConnection()

# @pytest.fixture(scope="session", autouse=True)
# def cleanup_test_database():
#     yield
#     try:
#         os.remove(TEST_DB_PATH)
#         print(f"Deleted {TEST_DB_PATH}")
#     except PermissionError as e:
#         print(f"Warning: Could not delete {TEST_DB_PATH}. It may still be in use. Error: {e}")

# def test_insertStartSession(db):
#     session_id = str(uuid.uuid4())
#     db.insertStartSession(session_id, "2025-02-26 05:00:00")

#     conn = db.getConnection()
#     with conn:
#         cur = conn.cursor()
#         cur.execute(
#             "SELECT * FROM GameSession WHERE sessionID = ?", (session_id,)
#         )
#         result = cur.fetchone()
    
#     assert result is not None
#     assert result[0] == session_id
#     assert result[1] == "2025-02-26 05:00:00"

#     conn.close()

# def test_InsertInteraction(db):
#     session_id = str(uuid.uuid4())
#     db.insertStartSession(session_id, "2025-02-26 05:00:00")

#     interaction_id = db.insertInteraction("2025-02-26 05:00:00", "2025-02-26 05:05:00", "Hi, my name is Jack", "Nice to meet you, Jack!", session_id, None)

#     conn = db.getConnection()
#     with conn:
#         cur = conn.cursor()
#         cur.execute(
#             "SELECT * FROM Interaction WHERE sessionID = ?", (session_id,)
#         )
#         result = cur.fetchone()

#     assert result is not None
#     assert result[3] == "Hi, my name is Jack"
#     assert result[4] == "Nice to meet you, Jack!"

#     conn.close()

# def test_fetchConversation(db):
#     session_id = str(uuid.uuid4())
#     db.insertStartSession(session_id, "2025-02-26 10:00:00")

#     db.insertInteraction("2025-02-26 10:05:00", "2025-02-26 10:10:00", "Hello", "Hi", session_id, None)
#     db.insertInteraction("2025-02-26 10:15:00", "2025-02-26 10:20:00", "How are you?", "Good", session_id, None)

#     conn = db.getConnection()
#     with conn:
#         cur = conn.cursor()
#         cur.execute(
#             "SELECT userInput, response FROM Interaction WHERE sessionID = ?", (session_id,)
#         )
#         conversation = cur.fetchall()

#     assert len(conversation) == 2
#     assert conversation[0] == ("Hello", "Hi")
#     assert conversation[1] == ("How are you?", "Good")

#     conn.close()

# def test_insertBiometrics(db):
#     session_id = str(uuid.uuid4())
#     db.insertStartSession(session_id, "2025-02-26 10:00:00")

#     interaction_id = str(uuid.uuid4())

#     db.insertBiometrics("2025-02-26 10:05:00", "2025-02-26 10:10:00", 0.5, 98.6, 72, 0.8, session_id, interaction_id)

#     conn = db.getConnection()
#     with conn:
#         cur = conn.cursor()
#         cur.execute(
#             "SELECT * FROM BiometricFeedback WHERE sessionID = ?", (session_id,)
#         )
#         result = cur.fetchone()

#     assert result is not None
#     assert result[3] == 0.5  # stdDeviation
#     assert result[4] == 98.6  # temperature
#     assert result[5] == 72  # heartRate
#     assert result[6] == 0.8 # skinConductance

#     conn.close()

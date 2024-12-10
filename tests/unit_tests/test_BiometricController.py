import unittest
from unittest.mock import patch, MagicMock
from BiometricSystem.BiometricController import BiometricController

class TestBiometricController(unittest.TestCase):

    def setup(self):
        self.mockGameController = MagicMock()
        self.mockDatabaseController = MagicMock()
        self.mockBiometricReader = MagicMock()

    def test_read_is_true(self):
        pass

    def test_read_fails(self):
        pass

    def test_reconnect(self):
        pass

    def test_isNervous(self):
        pass

    def test_setNervous(self):
        pass

    def test_sendToDB(self):
        pass


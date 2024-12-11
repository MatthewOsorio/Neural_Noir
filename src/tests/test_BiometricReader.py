import unittest
from BiometricSystem.BiometricReader import BiometricReader

class TestBiometricReader(unittest.TestCase):
    
    def setUp(self):
        self.biometric_reader = BiometricReader()
    
    def test_read(self):
        pass

    def test_processdata(self):
        pass
    
    def test_filterppg(self):
        pass
    
    def test_filterEDA(self):
        pass
    
    def test_calculateheartrate(self):
        pass
    
if __name__ == "__main__":
    unittest.main()
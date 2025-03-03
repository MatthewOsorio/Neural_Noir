class PTT:
    def __init__ (self, base):
        self.base = base
        self.pttActive = False
        self.button = None

    def setButton(self, button):
        self.button = button

    def showPTTButton(self):
        self.button.show()
        self.pttActive = True
    
    def hidePTTButton(self):
        self.button.hide()
        self.pttActive = False

    def getPTTActive(self):
        return self.pttActive

    
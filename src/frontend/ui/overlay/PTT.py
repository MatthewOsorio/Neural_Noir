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
    
    def setInactive(self):
        self.pttActive = False
        self.hidePTTButton()
        print("PTT Inactive")

    def getPTTActive(self):
        return self.pttActive

    
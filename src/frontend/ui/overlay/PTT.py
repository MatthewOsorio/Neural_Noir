class PTT:
    def __init__ (self, base):
        self.base = base
        self.pttActive = False
        self.button = None
        self.noError = True

    def setButton(self, button):
        self.button = button

    def showPTTButton(self):
        if self.noError == True:
            self.button.show()
            self.pttActive = True
        elif self.noError == False:
            self.button.hide()
            self.pttActive = False
    
    def hidePTTButton(self):
        self.button.hide()
    
    def setInactive(self):
        self.pttActive = False
        self.hidePTTButton()
        print("PTT Inactive")

    def getPTTActive(self):
        return self.pttActive
    
    def pttCountdown(self):
        countdown = 10
        if countdown == 0:
            return False

    
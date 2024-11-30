from direct.showbase.ShowBase import ShowBase
from ui.connectionDisplay import ConnectionDisplay

class TestApp(ShowBase):
    def __init__(self):
        super().__init__()
        # Initialize the ConnectionDisplay class
        self.connDisplay = ConnectionDisplay(self)

        # Test a specific method
        self.connDisplay.displayInternetOffline()

# Run the test application
app = TestApp()
app.run()
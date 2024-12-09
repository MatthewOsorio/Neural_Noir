from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectButton import DirectButton
from ui.subtitles import Subtitles

# Mock the manager and gameController classes
class MockManager:
    pass

class MockInterrogationRoomResponse:
    def __init__(self):
        self.responses = [
            "This is the first response from the detective.",
            "Here comes another response during the interrogation.",
            "Final response to conclude the interrogation session."
        ]
        self.current_index = 0

    def runInterrogation(self):
        if self.current_index < len(self.responses):
            response = self.responses[self.current_index]
            self.current_index += 1
            return response
        return "No more responses."

class TestSubtitlesApp(ShowBase):
    def __init__(self):
        super().__init__()
        self.manager = MockManager()
        self.interrogationRoomResponse = MockInterrogationRoomResponse()

        # Initialize Subtitles
        self.subtitles = Subtitles(
            self.manager,
            gameController=None,  # Mock or pass None if unused
            interrogationRoomResponse=self.interrogationRoomResponse
        )

        # Add a button to toggle subtitles
        self.toggleButton = DirectButton(
            text="Toggle Subtitles",
            scale=0.1,
            command=self.toggleSubtitles
        )

        # Hide subtitles initially
        self.subtitles.hideSubtitles()

    def toggleSubtitles(self):
        if self.subtitles.subtitleDisplay.isHidden():
            self.subtitles.showSubtitles()
        else:
            self.subtitles.hideSubtitles()

# Run the test app
app = TestSubtitlesApp()
app.run()

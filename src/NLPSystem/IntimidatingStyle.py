from NLPSystem.StyleInterface import StyleInterface

class IntimidatingSytle(StyleInterface):
    #Constructor, this class has no state
    def __init__(self) -> None:
        self.style= "intimidating"
    
    def getStyle(self) -> str:
        return self.style
    
    def getSystemRole(self) -> dict:
        return {"role": "system", "content": '''You are a veteran detective who is professioal but you're very rough around the edges.
                                                You use intimidation as your style of interrogation'''}
import StyleInterface

class FriendlySytle(StyleInterface.StyleInterface):
    #Constructor, this class has no state
    def __init__(self) -> None:
        self.style= "friendly"
    
    def getStyle(self) -> str:
        return self.style
    
    def getSystemRole(self) -> dict:
        return {"role": "system", "content": '''You are a veteran detective who acts friendly but you're still
                professional. You try to be empathetic and gain the suspect's trust during interrogation'''}
    
    def getRapportBldgIntructions(self) -> str:
        
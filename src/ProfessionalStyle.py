import StyleInterface

class ProfessionalStyle(StyleInterface.StyleInterface):
    #Constructor, this class has no state
    def __init__(self):
        self.style= "professional"
    
    def getStyle(self):
        return self.style
    
    def getSystemRole(self) -> dict:
        return {"role": "system", "content": "You are a veteran detective who acts professsionally but you're a still serious. You do everything by the book."}
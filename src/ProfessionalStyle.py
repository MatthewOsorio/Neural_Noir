import NLPInterface

class ProfessionalStyle(NLPInterface.NLPInterface):
    #Constructor, this class has no state
    def __init__(self):
        self.style= "professional"
    
    def getStyle(self):
        return self.style
    
    def getSystemRole(self):
        return {"role": "system", "content": "You are a veteran detective who acts professsionally but you're a little rough around the edges."}
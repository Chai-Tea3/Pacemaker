class User:
    def __init__(self,username: str,password: str,pacing: str,parameters: dict[str: float]) -> str: # Initiates a class for each user to hold their information
        self.username = str(username)
        self.password = str(password)
        self.pacing = str(pacing)
        self.parameters = parameters
        
    def getUsername(self) -> str:
        return self.username #returns username
    
    def getPassword(self) -> str:
        return self.password #returns password
    
    def getParameters(self)-> dict[str: float]:
        return self.parameters

    def getParameter(self,index)-> float:
        return self.parameters[index]

    def getPacing(self)-> int:
        if(self.pacing == "AOO"):
            return 1
        elif(self.pacing == "VOO"):
            return 2
        elif(self.pacing == "AAI"):
            return 3
        elif(self.pacing == "VVI"):
            return 4
        elif(self.pacing == "AOOR"):
            return 5
        elif(self.pacing == "VOOR"):
            return 6
        elif(self.pacing == "AAIR"):
            return 7
        elif(self.pacing == "VVIR"):
            return 8
        elif(self.pacing == "IDLE"):
            return 0
    
    def setParameter(self,value: float, index: int):
        self.parameters[index] = float(value)

    def setPacing(self,value: str):
        self.pacing = value

        
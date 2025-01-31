from enum import Enum
from parameters import Parameter

class Pacing(Enum):
    #enums each of the used pacing modes for part 1, gives each a list of parameter values 
    VOO = "Ventricular", [
        Parameter.LRL,
        Parameter.URL,
        Parameter.VA,
        Parameter.VPW,
        Parameter.VRP,
    ]
    VVI = "Ventricular", [
       Parameter.LRL,
       Parameter.URL,
       Parameter.VA,
       Parameter.VPW,
       Parameter.VRP, 
    ]
    AOO = "Atrial", [
        Parameter.LRL,
        Parameter.URL,
        Parameter.AA,
        Parameter.APW,
        Parameter.ARP,
    ]
    AAI = "Atrial", [
        Parameter.LRL,
        Parameter.URL,
        Parameter.AA,
        Parameter.APW,
        Parameter.ARP,
    ]
    IDLE = "IDLE", [
        Parameter.LRL,
        Parameter.URL,
        Parameter.AA,
        Parameter.APW,
        Parameter.ARP,
    ]

    def __init__(self,title: str, parameterlist: list):
        self.title = str(title)
        self.parameters = list(parameterlist) 
    #initializes the values, giving each a title and list of parameters

    def getName(self)-> str:
        return self.name
    #returns the name ("VOO", "VVI")
    
    def getTitle(self)-> str:
        return self.title
    #returns the title, ("Ventricular", "Atrial")

    
    def getParameters(self):
        return self.parameters
    #returns the full list of parameters

    @classmethod
    def InitialUserValues(cls)-> str:
        return Pacing.IDLE.getName()
    #for the user, gives the name of the initial value, for assignment 1 returns "AOO", for final iteration will return initial value for 
    #user registration, different user function to returning or changing the users pacing mode
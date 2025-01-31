from enum import Enum
class Parameter(Enum):
    #enums each type of parameter in the class, giving each a name, nominal value and unit
    LRL = 'lower_rate_limit', 60, 'ppm'
    URL = 'upper_rate_limit', 120, 'ppm'
    AA = "atrial_amplitude", 3.5, 'V'
    APW = "atrial_pulse_width", 0.4, 'ms'
    ARP = "atrial_refractory_period",250, 'ms'
    AS = "Atrial_sensitivity",0,"V"
    VA = "ventricular_amplitude", 3.5, 'V'
    VPW = "ventricular_pulse width", 0.4, "ms"
    VRP = "ventricular_refractory_period", 320, 'ms'
    VS = "Ventricular_sensitivity",0,"V"
    HRL = "Hysterisis_Rate_Limit", 0,''
    HINT = "Hysterisis_Interval", 0, "ppm"
    AT = "Activity_Threshold", 15,""
    REAC = "Reaction_Time", 10,"s"
    RES = "Response_Factor", 8,""
    REC = "Recovery_Time", 5,"min"
    MSR = "Maximum_sensor_rate",60,"ppm"

    def __init__(self,title: str, nominal: float, unit: str):
        self.title = str(title)
        self.nominal = float(nominal) 
        self.unit = str(unit) 
    #initiates the values (will add values other than nominal during assignment 2)

    def getName(self)-> str:
        return self.name
        #returns the name (for LRL it will return "LRL")
    
    def getTitle(self)-> str:
        return self.title
        #returns the name (for LRL it will return " lower_rate_limit")
    def getUnit(self)-> str:
        return self.unit
    # returns the unit ("ppm","ms")
    def getNominalvalue(self):
        return self.nominal 
    #returns the nominal values for each variable

    @classmethod
    def UserValues(cls)-> dict[str:float]:
        return {parameter.getName(): parameter.getNominalvalue() for parameter in Parameter}
    #for saving in the json file, calls the name of the parameter (LRL etc), and the nominal values. 
    # this is used to set an intial value for each user
class Egram:
    #init for all egram values
    def __init__(self):
        self.atrial = 1
        self.ventricular = 1
        self.gain = float(0.5)
        self.highPass = True
    
    #returning values of egram to be used later
    def getGain(self):
        return self.gain
    
    def getHighPass(self):
        return self.highPass
    
import random

class Helper:
    
    def GetRandom(self, valFrom, valTo, isBwZeroAndOne):
        value = random.randint(valFrom, valTo)
        if isBwZeroAndOne:
            value = value/100
        return value
    
    def GetColors(self, isRandom):
        colorArr = [0.5, 0.5, 0.5]
        if isRandom:
            colorArr = [self.GetRandom(0,101, True), self.GetRandom(0,101, True), self.GetRandom(0,101, True)]
        return colorArr

    def GetRandomAbsolutePosition(self, isRandom):
        position = [0, 0, 0.9]
        if isRandom:
            #position = [self.GetRandom(0,20,True), self.GetRandom(-45,60,True), self.GetRandom(50,80,True)] #100-120 jobb
            position = [self.GetRandom(-10, 20, True), self.GetRandom(-25, 60, True), 1.1]#DGU: z pos was increased in order to avoid the bug of bin movement - 20200920
        return position
    
    def GetRandomAbsoluteOrientation(self, isRandom):
        orientation = [0, 35, 35]
        if isRandom: 
             orientation = [self.GetRandom(0,360,True), self.GetRandom(0,360,True), self.GetRandom(0,360,True)]
        return orientation

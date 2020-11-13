import random
import Query.quaternions as quat
import numpy as np

class Helper:
    
    def GetRandom(self, valFrom, valTo, isBwZeroAndOne):
        value = random.randint(valFrom, valTo)
        if isBwZeroAndOne:
            value = value/100
            #value = value/abs(valTo-valFrom)
        return value
    
    def GetColors(self, isRandom):
        colorArr = [0.5, 0.5, 0.5]
        if isRandom:
            colorArr = [self.GetRandom(0,101, True), self.GetRandom(0,101, True), self.GetRandom(0,101, True)]
        return colorArr

    def GetRandomAbsolutePosition(self, isRandom):
        position = [0, 0, 0.9]
        if isRandom:
            position = [self.GetRandom(-10, 20, True), self.GetRandom(-25, 60, True), 0.9]#DGU: change the z position if the bin is removed
        return position
    
    def GetRandomAbsoluteOrientation(self, isRandom):
        orientation = [0, 35, 35]
        if isRandom:
            # orientation = [self.GetRandom(0,360,True), self.GetRandom(0,360,True), self.GetRandom(0,360,True)]
            temp = self.GetRandom(0, 360, False)
            if temp > 180:
                y = 90
            else:
                y = -90
            #orientation = [self.GetRandom(0, 360, True), y, self.GetRandom(0, 360, True)]
            orientation = [0, y, 0]
        return orientation

    def RotateRandomObject(self, isRandom):
        if isRandom:
            rotate_x = self.GetRandom(0, 360, False)
            angleMx = [rotate_x, 0, 0]
            translationMx = [0,0,0]
            rotation = quat.TransformationMatrix(angleMx, translationMx)
            rotationMx = np.transpose(rotation)
        return rotationMx
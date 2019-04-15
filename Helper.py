import random

class Helper:
    @staticmethod
    def GetRandom(valFrom, valTo, isBwZeroAndOne):
        value = random.randint(valFrom, valTo)
        if isBwZeroAndOne:
            value = value/100
        return value
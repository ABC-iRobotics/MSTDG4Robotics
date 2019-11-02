import sys, os, glob
import Helper as hp

class VrepMeshDrawer:
    
    def __init__(self, vrepConn,binPickingScene, functionName='insertMesh', folderName = 'meshes/' ):
        self.functionName = functionName
        self.vrepConn = vrepConn
        self.folderName = folderName    
        self.binPickingScene = binPickingScene

    def GetMeshList(self):
        globalPath = os.path.dirname(__file__)
        fileNames = glob.glob( globalPath +'/../' +self.folderName + "*.stl")
        return fileNames

    def GetColors(self, isRandom):
        colorArr = [0.5, 0.5, 0.5]
        if isRandom:
            colorArr = [hp.Helper.GetRandom(0,101, True),hp.Helper.GetRandom(0,101, True),hp.Helper.GetRandom(0,101, True)]
        return colorArr
    
    def GetScaling(self, isRandom):
        scale = 0.004
        if isRandom:
            scale = 3*hp.Helper.GetRandom(0,101, True)
        return scale

    def GetAbsolutePosition(self, isRandom):
        position = [0, 0, 0.9]
        if isRandom:
            position = [hp.Helper.GetRandom(0,20,True), hp.Helper.GetRandom(-45,60,True), hp.Helper.GetRandom(50,80,True)]
        return position

    def GetAbsoluteOrientation(self, isRandom):
        orientation = [0, 35, 35]
        if isRandom: 
             orientation = [hp.Helper.GetRandom(0,360,True), hp.Helper.GetRandom(0,360,True), hp.Helper.GetRandom(0,360,True)]
        return orientation

    def DrawMesh(self):
        meshList = self.GetMeshList()
        
        floatParamList = self.GetColors(True)
        scale = self.GetScaling(False)
        floatParamList.append(scale)
        floatParamList.extend(self.GetAbsolutePosition(True))
        floatParamList.extend(self.GetAbsoluteOrientation(True))

        separator = ',\n'
        print('Call '+self.functionName+ ' with '+ separator.join(meshList)+' parameter.')
        ret, ints, floats, strings, buffs = self.vrepConn.callScript(self.functionName, inStrings=meshList, inFloats=floatParamList)
        return ret, ints, floats, strings, buffs
        

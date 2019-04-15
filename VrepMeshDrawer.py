import sys
import VrepConnector
import glob
import os
import Helper as hp

class VrepMeshDrawer:
    
    def __init__(self, scriptDescription='remoteApiCommandServer', functionName='insertMesh', folderName = 'meshes/'):
        self.scriptDescription = scriptDescription
        self.functionName = functionName
        self.vrepConn = VrepConnector.VrepConnector()
        self.folderName = folderName
        

    def GetMeshList(self):
        globalPath = os.path.dirname(__file__)
        fileNames = glob.glob( globalPath +'/' +self.folderName + "*.stl")
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
            position = [hp.Helper.GetRandom(0,20,True), hp.Helper.GetRandom(0,20,True), hp.Helper.GetRandom(95,115,True)]
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
        print('Call '+self.functionName+ ' in '+self.scriptDescription + ' with '+ separator.join(meshList)+' parameter.')
        ret, ints, floats, strings, buffs = self.vrepConn.callScript(self.functionName, self.scriptDescription, inStrings=meshList, inFloats=floatParamList)
        return ret, ints, floats, strings, buffs

    def GetObjectProperties(self, name, objectHandleList):
        for i in objectHandleList:
            self.vrepConn.vrep.simxSetModelProperty(self.vrepConn.clientID, i, 0, self.vrepConn.vrep.simx_opmode_blocking)
            self.vrepConn.vrep.simxSetObjectIntParameter(self.vrepConn.clientID, i, self.vrepConn.vrep.sim_shapeintparam_static, 0, self.vrepConn.vrep.simx_opmode_blocking)
            self.vrepConn.vrep.simxSetObjectIntParameter(self.vrepConn.clientID, i, self.vrepConn.vrep.sim_shapeintparam_respondable, 1, self.vrepConn.vrep.simx_opmode_blocking)
    
    def GetObjects(self, name, count):
        objectHandleList = []
        if count < 1: 
            return -1
        objectHandle = self.vrepConn.vrep.simxGetObjectHandle(self.vrepConn.clientID, name, self.vrepConn.vrep.simx_opmode_blocking)[1]
        objectHandleList.append(objectHandle)
        if count > 1:
            i = 0
            while objectHandle != 0:
                objectHandle = self.vrepConn.vrep.simxGetObjectHandle(self.vrepConn.clientID, (name+str(i)), self.vrepConn.vrep.simx_opmode_blocking)[1]
                if(objectHandle != 0):
                    objectHandleList.append(objectHandle)
                    i+=1
        return 0, objectHandleList

        

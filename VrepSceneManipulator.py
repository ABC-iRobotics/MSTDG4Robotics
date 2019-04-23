import sys
import VrepConnector
import glob
import os
import time
import Helper as hp

class VrepSceneManipulator:

    def __init__(self):
        self.vrepConn = VrepConnector.VrepConnector()

    def SetObjectsToDynamic(self, name, objectHandleList):
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

    def RePaintElement(self, elementName,isRandom):
        floats = [0.5, 0.5, 0.5]
        if isRandom:
            floats = [hp.Helper.GetRandom(0, 101, True), hp.Helper.GetRandom(0, 101, True), hp.Helper.GetRandom(0, 101, True)]
        strings = [elementName]
        self.vrepConn.callScript('setColor', inStrings=strings, inFloats=floats)
        return 0

    def GetImage(self, visionSensorName):
        time.sleep(2)
        handle = self.vrepConn.vrep.simxGetObjectHandle(self.vrepConn.clientID, visionSensorName, self.vrepConn.vrep.simx_opmode_blocking)[1]
        result, resolution, image= self.vrepConn.vrep.simxGetVisionSensorImage(self.vrepConn.clientID, handle, 0, self.vrepConn.vrep.simx_opmode_streaming)
        if result == self.vrepConn.vrep.simx_return_ok:
            imageAcquisitionTime=self.vrepConn.vrep.simxGetLastCmdTime(self.vrepConn.clientID)
        else:
            print('VrepSceneManipulator: GetImage: Error while get the image sensor image')
        return 0

    
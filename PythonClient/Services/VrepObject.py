import sys, os, glob, array, datetime, time
import Services.VrepConnector as vcon
import Helper as hp
from PIL import Image

class VrepObject:

    def __init__(self, vrepConnector, name):
        self.vrepConn = vrepConnector
        self.opMode = self.vrepConn.vrepConst.simx_opmode_blocking
        self.clientID = vrepConnector.clientID
        self.returnOK = vrepConnector.vrepConst.simx_return_ok
        self.name = name
        self.handler = self.GetObject(name)
        self.position = None
        self.orientation = None

    def GetObject(self, name):
        handleErr, handle = self.vrepConn.vrep.simxGetObjectHandle(self.clientID, name, self.opMode)
        if handleErr != self.returnOK:
            print("ERROR: VrepObject: GetObject")
        return handle
    
    def GetObjectPositionAndOrientation(self, referenceName = None):
        if self.position is not None and self.orientation is not None:
            return self.position, self.orientation
        elif self.handler > -1:
            position = []
            orientation = []
            handle = self.handler
            if referenceName is None:
                posReturnCode, position = self.vrepConn.vrep.simxGetObjectPosition(self.clientID, handle, -1, self.opMode)
                orReturnCode, orientation = self.vrepConn.vrep.simxGetObjectOrientation(self.clientID, handle, -1, self.opMode)
                if posReturnCode == self.returnOK and orReturnCode == self.returnOK:
                    self.position = position
                    self.orientation = orientation
                    return position, orientation
                else:
                    return -1, "ERROR: Get position and orientation failed"
            else:
                refHandleErr, refHandle = self.vrepConn.vrep.simxGetObjectHandle(self.clientID, referenceName, self.opMode)
                if refHandleErr == self.returnOK:
                    posReturnCode, position = self.vrepConn.vrep.simxGetObjectPosition(self.clientID, handle, refHandle, self.opMode)
                    orReturnCode, orientation = self.vrepConn.vrep.simxGetObjectOrientation(self.clientID, handle, refHandle, self.opMode)
                    if posReturnCode == self.returnOK and orReturnCode == self.returnOK:
                        self.position = position
                        self.orientation = orientation
                        return position, orientation
                    else:
                        return -1, "ERROR: Get position and orientation failed"
                else:
                    return -1, "ERROR: Get reference handler failed"
    
    def Repaint(self, colorFloats):
        if self.handler > -1:
            self.vrepConn.callScript('setColor', inStrings=[self.name], inFloats=colorFloats)

    def Remove(self):
        if self.handler > -1:
            self.vrepConn.vrep.simxRemoveObject(self.clientID, self.handler, self.opMode)
            print('VrepSceneManipulator: Object successfully deleted: ' + self.name)

    def SetToDynamic(self):
        if self.handler > -1:
            self.vrepConn.vrep.simxSetModelProperty(self.clientID, self.handler, 0, self.opMode)
            self.vrepConn.vrep.simxSetObjectIntParameter(self.clientID, self.handler, self.vrepConn.vrepConst.sim_shapeintparam_static, 0, self.opMode)
            self.vrepConn.vrep.simxSetObjectIntParameter(self.clientID, self.handler, self.vrepConn.vrepConst.sim_shapeintparam_respondable, 1, self.opMode)
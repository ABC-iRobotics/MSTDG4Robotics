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
        self.size = None

    def GetObject(self, name):
        handleErr, handle = self.vrepConn.vrep.simxGetObjectHandle(self.clientID, name, self.opMode)
        if handleErr != self.returnOK:
            print("ERROR: VrepObject: GetObject")
        return handle

    def GetObjectPosition(self):
        handleErr, handle = self.vrepConn.vrep.simxGetObjectHandle(self.clientID, self.name, self.opMode)
        if handleErr != self.returnOK:
            print("ERROR: VrepObject: GetObject")
        posReturnCode, position = self.vrepConn.vrep.simxGetObjectPosition(self.clientID, handle, -1, self.opMode)
        if posReturnCode == self.returnOK:
            self.position = position
            return position
        else:
            return -1, "ERROR: Get position failed"
        return handle


    def SetObjectPosition(self, position):
        handleErr, handle = self.vrepConn.vrep.simxGetObjectHandle(self.clientID, self.name, self.opMode)
        if handleErr != self.returnOK:
            print("ERROR: VisionSensor: Set its height")
        posReturnCode = self.vrepConn.vrep.simxSetObjectPosition(self.clientID, handle, -1, position, self.opMode)
        if posReturnCode != self.returnOK:
            return -1, "ERROR: Get position failed"


    def GetObjectSize(self, clientID, opMode):
        if self.handler > -1:
            handle = self.handler
            minxReturnCode, minx = self.vrepConn.vrep.simxGetObjectFloatParameter(clientID, handle, 15, opMode)  # get minx
            minyReturnCode, miny = self.vrepConn.vrep.simxGetObjectFloatParameter(clientID, handle, 16, opMode)  # get miny
            minzReturnCode, minz = self.vrepConn.vrep.simxGetObjectFloatParameter(clientID, handle, 17, opMode)  # get minz
            maxxReturnCode, maxx = self.vrepConn.vrep.simxGetObjectFloatParameter(clientID, handle, 18, opMode)  # get maxx
            maxyReturnCode, maxy = self.vrepConn.vrep.simxGetObjectFloatParameter(clientID, handle, 19, opMode)  # get maxy
            maxzReturnCode, maxz = self.vrepConn.vrep.simxGetObjectFloatParameter(clientID, handle, 20, opMode)  # get maxz
            obj_x = maxx - minx
            obj_y = maxy - miny
            obj_z = maxz - minz
            sizeReturnCode = minxReturnCode and minyReturnCode and minzReturnCode and maxxReturnCode and maxyReturnCode and maxzReturnCode
            size = [obj_x, obj_y, obj_z]
        if sizeReturnCode == self.returnOK:
            return size
        else:
            return -1, "ERROR: Get object size failed"

    def GetVisionSensorAngle(self, clientID, opMode):
        if self.handler > -1:
            handle = self.handler
            angleRetunrCode, angle = self.vrepConn.vrep.simxGetObjectFloatParameter(clientID, handle, 1004, opMode)  # get perspective angle in rad
        if angleRetunrCode == self.returnOK:
            return angle
        else:
            return -1, "ERROR: Get vision sensor perspective angle failed"

    def GetObjectPositionAndOrientation(self, referenceName = None):
        # Commented: This condition was true after the second call (first: relative, second:absolute) therefore abs position was not received correctly
        # if self.position is not None and self.orientation is not None and self.size is not None:
        #     return self.position, self.orientation, self.size
        # elif self.handler > -1:
        if self.handler > -1:
            position = []
            orientation = []
            size = []
            handle = self.handler
            if referenceName is None:
                posReturnCode, position = self.vrepConn.vrep.simxGetObjectPosition(self.clientID, handle, -1, self.opMode)
                orReturnCode, orientation = self.vrepConn.vrep.simxGetObjectQuaternion(self.clientID, handle, -1, self.opMode) #get in absolut coordinate-system
                size = self.GetObjectSize(self.clientID, self.opMode)
                if posReturnCode == self.returnOK and orReturnCode == self.returnOK:
                    self.position = position
                    self.orientation = orientation
                    self.size = size
                    return position, orientation, size
                else:
                    return -1, "ERROR: Get position and orientation failed"
            else:
                refHandleErr, refHandle = self.vrepConn.vrep.simxGetObjectHandle(self.clientID, referenceName, self.opMode)
                if refHandleErr == self.returnOK:
                    posReturnCode, position = self.vrepConn.vrep.simxGetObjectPosition(self.clientID, handle, refHandle, self.opMode)
                    orReturnCode, orientation = self.vrepConn.vrep.simxGetObjectQuaternion(self.clientID, handle, refHandle, self.opMode)
                    size = self.GetObjectSize(self.clientID, self.opMode)
                    if posReturnCode == self.returnOK and orReturnCode == self.returnOK:
                        self.position = position
                        self.orientation = orientation
                        self.size = size
                        return position, orientation, size
                    else:
                        return -1, "ERROR: Get position and orientation failed"
                else:
                    return -1, "ERROR: Get reference handler failed"
    
    def SetColor(self, colorFloats):
        if self.handler > -1:
            self.vrepConn.callScript('setColor', inStrings=[self.name], inFloats=colorFloats)
    
    def SetTransparency(self, opacity):
        if self.handler > -1:
            self.vrepConn.callScript('setTransparency', inStrings=[self.name], inFloats=[opacity])

    def Remove(self):
        if self.handler > -1:
            self.vrepConn.vrep.simxRemoveObject(self.clientID, self.handler, self.opMode)
            print('VrepSceneManipulator: Object successfully deleted: ' + self.name)

    def SetToDynamic(self):
        if self.handler > -1:
            self.vrepConn.vrep.simxSetModelProperty(self.clientID, self.handler, 0, self.opMode)
            self.vrepConn.vrep.simxSetObjectIntParameter(self.clientID, self.handler, self.vrepConn.vrepConst.sim_shapeintparam_static, 0, self.opMode)
            self.vrepConn.vrep.simxSetObjectIntParameter(self.clientID, self.handler, self.vrepConn.vrepConst.sim_shapeintparam_respondable, 1, self.opMode)

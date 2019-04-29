import sys, os, glob, array, datetime, time
import Services.VrepConnector as vcon
import Helper as hp
from PIL import Image

class VrepSceneManipulator:

    def __init__(self):
        self.vrepConn = vcon.VrepConnector()

    def SetObjectsToDynamic(self, name, objectHandleList):
        for i in objectHandleList:
            self.vrepConn.vrep.simxSetModelProperty(self.vrepConn.clientID, i, 0, self.vrepConn.vrepConst.simx_opmode_blocking)
            self.vrepConn.vrep.simxSetObjectIntParameter(self.vrepConn.clientID, i, self.vrepConn.vrepConst.sim_shapeintparam_static, 0, self.vrepConn.vrepConst.simx_opmode_blocking)
            self.vrepConn.vrep.simxSetObjectIntParameter(self.vrepConn.clientID, i, self.vrepConn.vrepConst.sim_shapeintparam_respondable, 1, self.vrepConn.vrepConst.simx_opmode_blocking)
    
    def GetObjects(self, name, count):
        objectHandleList = []
        if count < 1: 
            return -1
        objectHandle = self.vrepConn.vrep.simxGetObjectHandle(self.vrepConn.clientID, name, self.vrepConn.vrepConst.simx_opmode_blocking)[1]
        objectHandleList.append(objectHandle)
        if count > 1:
            i = 0
            while objectHandle != 0:
                objectHandle = self.vrepConn.vrep.simxGetObjectHandle(self.vrepConn.clientID, (name+str(i)), self.vrepConn.vrepConst.simx_opmode_blocking)[1]
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
        time.sleep(2) #approx falling time in rt settings
        handleErr, visionSensorHandle = self.vrepConn.vrep.simxGetObjectHandle(self.vrepConn.clientID, visionSensorName, self.vrepConn.vrepConst.simx_opmode_blocking)
        if handleErr == self.vrepConn.vrepConst.simx_return_ok:
            err, resolution, image = self.vrepConn.vrep.simxGetVisionSensorImage(self.vrepConn.clientID, visionSensorHandle, 0, self.vrepConn.vrepConst.simx_opmode_streaming)
            time.sleep(.1)

            while (self.vrepConn.vrep.simxGetConnectionId(self.vrepConn.clientID) != -1):
                err, resolution, image = self.vrepConn.vrep.simxGetVisionSensorImage(self.vrepConn.clientID, visionSensorHandle, 0, self.vrepConn.vrepConst.simx_opmode_buffer)       
                if err == self.vrepConn.vrepConst.simx_return_ok:
                    print('Successfully get an image from vision sensor.')
                    break
            image_byte_array = array.array('b',image).tobytes()
            im = Image.frombuffer("RGB", (resolution[0],resolution[1]), image_byte_array, "raw", "RGB", 0, 1)        
            
            #im.show() #just for testing

            depthReturnCode, depthResolution, depthBuffer = self.vrepConn.vrep.simxGetVisionSensorDepthBuffer(self.vrepConn.clientID, visionSensorHandle, self.vrepConn.vrepConst.simx_opmode_streaming)
            time.sleep(.1)
            while (self.vrepConn.vrep.simxGetConnectionId(self.vrepConn.clientID) != -1):
                depthReturnCode, depthResolution, depthBuffer = self.vrepConn.vrep.simxGetVisionSensorDepthBuffer(self.vrepConn.clientID, visionSensorHandle, self.vrepConn.vrepConst.simx_opmode_buffer)       
                if depthReturnCode == self.vrepConn.vrepConst.simx_return_ok:
                    print('Successfully get depth data from vision sensor.')
                    break

            currentDT = datetime.datetime.now()
            globalPath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'image_set'))
            path = os.path.join(globalPath, (str(currentDT)+'.jpg'))
            im.save(path)
            
            if err == self.vrepConn.vrepConst.simx_return_ok:
                #imageAcquisitionTime=self.vrepConn.vrep.simxGetLastCmdTime(self.vrepConn.clientID)
                print('VrepSceneManipulator: GetImage: Image saved successfully: '+path)
                return path, depthBuffer, depthResolution
            else:
                print('VrepSceneManipulator: GetImage: Error while get the image sensor image')
        else:
            print('VrepSceneManipulator: GetImage: Cannot get handler object')
        return 0

    def GetObjectPositionAndOrientation(self, name, referenceName):
        position = []
        orientation = []
        handleErr, handle = self.vrepConn.vrep.simxGetObjectHandle(self.vrepConn.clientID, name, self.vrepConn.vrepConst.simx_opmode_blocking)
        if handleErr == self.vrepConn.vrepConst.simx_return_ok:
            if referenceName is None:
                posReturnCode, position = self.vrepConn.vrep.simxGetObjectPosition(self.vrepConn.clientID, handle, -1, self.vrepConn.vrepConst.simx_opmode_blocking)
                orReturnCode, orientation = self.vrepConn.vrep.simxGetObjectOrientation(self.vrepConn.clientID, handle, -1, self.vrepConn.vrepConst.simx_opmode_blocking)
                if posReturnCode == self.vrepConn.vrepConst.simx_return_ok and orReturnCode == self.vrepConn.vrepConst.simx_return_ok:
                    return position, orientation
                else:
                    return -1, "ERROR: Get position and orientation failed"
            else:
                refHandleErr, refHandle = self.vrepConn.vrep.simxGetObjectHandle(self.vrepConn.clientID, referenceName, self.vrepConn.vrepConst.simx_opmode_blocking)
                if refHandleErr == self.vrepConn.vrepConst.simx_return_ok:
                    posReturnCode, position = self.vrepConn.vrep.simxGetObjectPosition(self.vrepConn.clientID, handle, refHandle, self.vrepConn.vrepConst.simx_opmode_blocking)
                    orReturnCode, orientation = self.vrepConn.vrep.simxGetObjectOrientation(self.vrepConn.clientID, handle, refHandle, self.vrepConn.vrepConst.simx_opmode_blocking)
                    if posReturnCode == self.vrepConn.vrepConst.simx_return_ok and orReturnCode == self.vrepConn.vrepConst.simx_return_ok:
                        return position, orientation
                    else:
                        return -1, "ERROR: Get position and orientation failed"
                else:
                    return -1, "ERROR: Get reference handler failed"
        else:
            return -1, "ERROR: Get target object handler failed"

    def RemoveObject(self, name):
        handleErr, handle = self.vrepConn.vrep.simxGetObjectHandle(self.vrepConn.clientID, name, self.vrepConn.vrepConst.simx_opmode_blocking)
        if handleErr == self.vrepConn.vrepConst.simx_return_ok:
            self.vrepConn.vrep.simxRemoveObject(self.vrepConn.clientID, handle, self.vrepConn.vrepConst.simx_opmode_blocking)
            print('VrepSceneManipulator: Object successfully deleted: ' + name)
            return True
        else:
            print('VrepSceneManipulator: Object successfully deleted: ' + name)
            return False
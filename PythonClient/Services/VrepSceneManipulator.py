import sys, os, glob, array, datetime, time
import Helper as hp
from PIL import Image

import Services.VrepObject as vo

class VrepSceneManipulator:

    def __init__(self, vrepConn, binPickingScene):
        self.vrepConn = vrepConn
        self.binPickingScene = binPickingScene

    def SetObjectsToDynamic(self, name, objectHandleList):
        for i in objectHandleList:
            self.vrepConn.vrep.simxSetModelProperty(self.vrepConn.clientID, i, 0, self.vrepConn.vrepConst.simx_opmode_blocking)
            self.vrepConn.vrep.simxSetObjectIntParameter(self.vrepConn.clientID, i, self.vrepConn.vrepConst.sim_shapeintparam_static, 0, self.vrepConn.vrepConst.simx_opmode_blocking)
            self.vrepConn.vrep.simxSetObjectIntParameter(self.vrepConn.clientID, i, self.vrepConn.vrepConst.sim_shapeintparam_respondable, 1, self.vrepConn.vrepConst.simx_opmode_blocking)
    
    def GetObjectHandleList(self, name, count, startIndex = None):
        objectHandleList = []
        if count < 1: 
            return -1
        i = startIndex
        if startIndex is None:
            objectHandle = self.vrepConn.vrep.simxGetObjectHandle(self.vrepConn.clientID, name, self.vrepConn.vrepConst.simx_opmode_blocking)[1]
            objectHandleList.append(objectHandle)
            i = 0
        if count > 1:
            while objectHandle != 0:
                objectHandle = self.vrepConn.vrep.simxGetObjectHandle(self.vrepConn.clientID, (name+str(i)), self.vrepConn.vrepConst.simx_opmode_blocking)[1]
                if(objectHandle != 0):
                    objectHandleList.append(objectHandle)
                    i+=1
        return 0, objectHandleList

    def GetObjectList(self, name, startIndex = None):
        objectList = []
        i = startIndex
        
        if startIndex is None:
            elem = vo.VrepObject(self.vrepConn, name) 
            objectList.append(elem)
            i = 0
        else:
            elem = vo.VrepObject(self.vrepConn, (name+str(i))) 
            objectList.append(elem)
            i += 1
        while elem.handler > 0:
            elem = vo.VrepObject(self.vrepConn, (name+str(i))) 
            if(elem.handler > 0):
                objectList.append(elem)
                i+=1
        return objectList

    def RePaintElement(self, element, isRandom):
        #element is a VrepObject
        floats = [0.5, 0.5, 0.5]
        if isRandom:
            floats = [hp.Helper.GetRandom(0, 101, True), hp.Helper.GetRandom(0, 101, True), hp.Helper.GetRandom(0, 101, True)]
        
        element.SetColor(floats)
        return 0

    def GetImage(self, visionSensorName):
        time.sleep(.05) #approx falling time in rt settings
        handleErr, visionSensorHandle = self.vrepConn.vrep.simxGetObjectHandle(self.vrepConn.clientID, visionSensorName, self.vrepConn.vrepConst.simx_opmode_blocking)
        if handleErr == self.vrepConn.vrepConst.simx_return_ok:
            err, resolution, image = self.vrepConn.vrep.simxGetVisionSensorImage(self.vrepConn.clientID, visionSensorHandle, 0, self.vrepConn.vrepConst.simx_opmode_streaming)
            time.sleep(.05)

            while (self.vrepConn.vrep.simxGetConnectionId(self.vrepConn.clientID) != -1):
                err, resolution, image = self.vrepConn.vrep.simxGetVisionSensorImage(self.vrepConn.clientID, visionSensorHandle, 0, self.vrepConn.vrepConst.simx_opmode_buffer)       
                if err == self.vrepConn.vrepConst.simx_return_ok:
                    print('Successfully get an image from vision sensor.')
                    break
            image_byte_array = array.array('b',image).tobytes()
            im = Image.frombuffer("RGB", (resolution[0],resolution[1]), image_byte_array, "raw", "RGB", 0, 1)        
            
            #im.show() #just for testing

            depthReturnCode, depthResolution, depthBuffer = self.vrepConn.vrep.simxGetVisionSensorDepthBuffer(self.vrepConn.clientID, visionSensorHandle, self.vrepConn.vrepConst.simx_opmode_streaming)
            time.sleep(.05)
            while (self.vrepConn.vrep.simxGetConnectionId(self.vrepConn.clientID) != -1):
                depthReturnCode, depthResolution, depthBuffer = self.vrepConn.vrep.simxGetVisionSensorDepthBuffer(self.vrepConn.clientID, visionSensorHandle, self.vrepConn.vrepConst.simx_opmode_buffer)       
                if depthReturnCode == self.vrepConn.vrepConst.simx_return_ok:
                    print('Successfully get depth data from vision sensor.')
                    break

            currentDT = datetime.datetime.now()
            globalPath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'image_set'))
            imgPath = os.path.join(globalPath, (currentDT.strftime("%Y_%m_%d_%H_%M_%S")+'.jpg'))
            im.save(imgPath)

            globalPath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'depth_set'))
            depthPath = os.path.join(globalPath, (currentDT.strftime("%Y_%m_%d_%H_%M_%S")+'.dat'))
            with open(depthPath, 'w') as f:
                for item in depthBuffer:
                    f.write("%f\n" % item)
            
            if err == self.vrepConn.vrepConst.simx_return_ok:
                #imageAcquisitionTime=self.vrepConn.vrep.simxGetLastCmdTime(self.vrepConn.clientID)
                print('VrepSceneManipulator: GetImage: Image saved successfully: ' + imgPath)
                return imgPath, depthPath, resolution
            else:
                print('VrepSceneManipulator: GetImage: Error while get the image sensor image')
        else:
            print('VrepSceneManipulator: GetImage: Cannot get handler object')
        return 0

    def RemoveObject(self, element):
        element.Remove()
        self.binPickingScene.RemoveShape()